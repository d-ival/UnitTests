import pytest
import app

class TestSecretaryGetInfo:

    def setup_class(self):
        app.directories = app.update_directories()
        app.documents = app.update_documents()

    @pytest.mark.parametrize('doc_num, etalon_result',[('11-2','Геннадий Покемонов'), ('010', None)])
    def test_get_doc_owner_name(self, doc_num, etalon_result):
        owner_name = app.get_doc_owner_name(doc_num)
        assert owner_name == etalon_result

    def test_get_all_doc_owners_names(self):
        result = app.get_all_doc_owners_names()
        uniq_owners = set([
            'Геннадий Покемонов', "Василий Гупкин", "Аристарх Павлов"
        ])
        assert len(uniq_owners.difference(result)) == 0

    def test_get_all_docs_info(self):
        result = app.get_all_docs_info()
        with open('fixtures\\all_docs_info.txt', encoding='utf8') as f:
            etalon = f.read()
            assert result == etalon

    @pytest.mark.parametrize('doc_num, etalon_result', [("2207 876234", '1'), ("10006", '2'), ("6809 282364", None)])
    def test_get_doc_shelf(self, doc_num, etalon_result):
        result = app.get_doc_shelf(doc_num)
        assert result == etalon_result

class TestSecretaryAddInfo:

    def setup(self):
        app.directories = {}
        app.documents = []

    def test_add_new_doc_shelf(self):
        result = app.add_new_doc('2207 876234', 'passport', 'Василий Гупкин', '1')
        assert result == '1'
        result = app.add_new_doc('11-2', 'invoice', 'Геннадий Покемонов', '1')
        assert result == '1'
        result = app.add_new_doc('10006', 'insurance', 'Аристарх Павлов', '2')
        assert result == '2'
        shelf_num, is_new = app.add_new_shelf(3)
        assert shelf_num == '3'
        assert is_new
        etalon_docs = app.update_documents()
        etalon_dirs = app.update_directories()
        assert app.documents == etalon_docs
        assert app.directories == etalon_dirs

class TestSecretaryDelInfo:

    def setup(self):
        app.directories = app.update_directories()
        app.documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"}
        ]

    def test_delete_doc_not_exists(self):
        result = app.delete_doc('789-00')
        assert result == None

    def test_delete_doc_exists(self):
        result = app.delete_doc('2207 876234')
        assert len(app.documents) == 0
