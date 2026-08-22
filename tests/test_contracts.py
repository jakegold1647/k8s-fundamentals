import os
import socket
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import main  # noqa: E402


def load_manifest(name):
    with (ROOT / "k8s" / name).open(encoding="utf-8") as manifest:
        return yaml.safe_load(manifest)


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = main.app.test_client()

    def test_root_uses_configured_greeting_and_hostname(self):
        with (
            patch.dict(os.environ, {"GREETING": "Howdy"}),
            patch.object(socket, "gethostname", return_value="hello-pod"),
        ):
            response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Howdy from hello-pod!\n")

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "ok\n")


class ManifestContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_manifest("configmap.yaml")
        cls.deployment = load_manifest("deployment.yaml")
        cls.service = load_manifest("service.yaml")

    def test_workload_and_service_select_the_same_pods(self):
        selector = self.deployment["spec"]["selector"]["matchLabels"]
        pod_labels = self.deployment["spec"]["template"]["metadata"]["labels"]

        self.assertEqual(selector, pod_labels)
        self.assertEqual(self.service["spec"]["selector"], pod_labels)

    def test_service_targets_the_container_port(self):
        container = self.deployment["spec"]["template"]["spec"]["containers"][0]
        container_port = container["ports"][0]["containerPort"]

        self.assertEqual(self.service["spec"]["ports"][0]["targetPort"], container_port)

    def test_greeting_comes_from_the_configmap(self):
        container = self.deployment["spec"]["template"]["spec"]["containers"][0]
        greeting = next(item for item in container["env"] if item["name"] == "GREETING")
        reference = greeting["valueFrom"]["configMapKeyRef"]

        self.assertEqual(reference["name"], self.config["metadata"]["name"])
        self.assertIn(reference["key"], self.config["data"])


if __name__ == "__main__":
    unittest.main()
