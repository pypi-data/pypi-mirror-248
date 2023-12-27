from setuptools import setup, find_packages

setup(
    name="mlflow-k8sstore-plugin",
    version="0.0.1",
    description="Test plugin for MLflow",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    # Require MLflow as a dependency of the plugin, so that plugin users can simply install
    # the plugin & then immediately use it with MLflow
    install_requires=["mlflow"],
    entry_points={
        "mlflow.model_registry_store": "k8s=mlflow_k8sstore.mlflow_k8sstore:K8sStore",
        # "mlflow.model_registry_store": "file-plugin=mlflow_test_plugin.sqlalchemy_store:PluginRegistrySqlAlchemyStore",
    },
)