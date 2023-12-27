from mlflow.store.model_registry.abstract_store import AbstractStore

class K8sStore(AbstractStore):

    def create_registered_model(self, name, tags=None, description=None):
        pass

    def update_registered_model(self, name, description):
        pass

    def rename_registered_model(self, name, new_name):
        pass

    def delete_registered_model(self, name):
        pass

    def search_registered_models(self, filter_string=None, max_results=None, order_by=None, page_token=None):
        pass

    def get_registered_model(self, name):
        pass

    def get_latest_versions(self, name, stages=None):
        pass

    def set_registered_model_tag(self, name, tag):
        pass

    def delete_registered_model_tag(self, name, key):
        pass

    def create_model_version(self, name, source, run_id=None, tags=None, run_link=None, description=None,
                             local_model_path=None):
        pass

    def update_model_version(self, name, version, description):
        pass

    def transition_model_version_stage(self, name, version, stage, archive_existing_versions):
        pass

    def delete_model_version(self, name, version):
        pass

    def get_model_version(self, name, version):
        pass

    def get_model_version_download_uri(self, name, version):
        pass

    def search_model_versions(self, filter_string=None, max_results=None, order_by=None, page_token=None):
        pass

    def set_model_version_tag(self, name, version, tag):
        pass

    def delete_model_version_tag(self, name, version, key):
        pass

    def set_registered_model_alias(self, name, alias, version):
        pass

    def delete_registered_model_alias(self, name, alias):
        pass

    def get_model_version_by_alias(self, name, alias):
        pass