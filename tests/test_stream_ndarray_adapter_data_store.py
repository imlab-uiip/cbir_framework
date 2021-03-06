import os
import unittest

from core.data_store.sqlite_table_datastore import SQLiteTableDataStore
from core.data_store.stream_ndarray_adapter_datastore import StreamNdarrayAdapterDataStore

from core.common.itertools_utils import *


class StreamNdarrayAdapterDataStoreTestCase(unittest.TestCase):
    """
         create temp database file and table in it with column type: ndarray
    """
    db_path = "temp_sqlite_db.sqlite"
    table_name = "temp_table"
    items = np.arange(10 * 5).reshape((10, 5))

    @classmethod
    def setUpClass(cls):
        with SQLiteTableDataStore(cls.db_path,
                                  cls.table_name, "ndarray") as sqltable_ds:
            sqltable_ds.save_items_sorted_by_ids(cls.items)

    @classmethod
    def tearDownClass(cls):
        with SQLiteTableDataStore(cls.db_path,
                                  cls.table_name, "ndarray") as sqltable_ds:
            sqltable_ds.drop(True)
        os.remove(cls.db_path)

    def test_setUpClass_tearDownClass(self):
        pass

    def test_get_count(self):
        sqltable_ds = SQLiteTableDataStore(StreamNdarrayAdapterDataStoreTestCase.db_path,
                                           StreamNdarrayAdapterDataStoreTestCase.table_name, "ndarray")
        adapter_ds = StreamNdarrayAdapterDataStore(sqltable_ds, detect_final_shape_by_first_elem=True)
        count_ = adapter_ds.get_count()
        self.assertEqual(len(StreamNdarrayAdapterDataStoreTestCase.items), count_)

    def test_get_ids_sorted(self):
        sqltable_ds = SQLiteTableDataStore(StreamNdarrayAdapterDataStoreTestCase.db_path,
                                           StreamNdarrayAdapterDataStoreTestCase.table_name, "ndarray")
        adapter_ds = StreamNdarrayAdapterDataStore(sqltable_ds, detect_final_shape_by_first_elem=True)
        ids_sorted = adapter_ds.get_ids_sorted()
        truth_ids = np.arange(len(StreamNdarrayAdapterDataStoreTestCase.items)) + 1
        self.assertTrue((truth_ids == ids_sorted).all())

    def test_get_items_sorted_by_ids(self):
        sqltable_ds = SQLiteTableDataStore(StreamNdarrayAdapterDataStoreTestCase.db_path,
                                           StreamNdarrayAdapterDataStoreTestCase.table_name, "ndarray")
        adapter_ds = StreamNdarrayAdapterDataStore(sqltable_ds, detect_final_shape_by_first_elem=True)
        items_sorted_by_ids = adapter_ds.get_items_sorted_by_ids()
        self.assertTrue((StreamNdarrayAdapterDataStoreTestCase.items == items_sorted_by_ids).all())

    def test_get_items_sorted_by_ids_with_slice(self):
        sqltable_ds = SQLiteTableDataStore(StreamNdarrayAdapterDataStoreTestCase.db_path,
                                           StreamNdarrayAdapterDataStoreTestCase.table_name, "ndarray")
        adapter_ds = StreamNdarrayAdapterDataStore(sqltable_ds, detect_final_shape_by_first_elem=True,
                                                   slice_get=(slice(None), slice(3)))
        items_sorted_by_ids = adapter_ds.get_items_sorted_by_ids()
        truth_items= StreamNdarrayAdapterDataStoreTestCase.items[:, :3]
        self.assertTrue(np.array_equal(items_sorted_by_ids,truth_items))

    def test_get_items_sorted_by_ids_items_bytes(self):

        sqltable_ds = SQLiteTableDataStore(StreamNdarrayAdapterDataStoreTestCase.db_path,
                                           StreamNdarrayAdapterDataStoreTestCase.table_name, "ndarray")
        adapter_ds = StreamNdarrayAdapterDataStore(sqltable_ds, detect_final_shape_by_first_elem=True)
        items_sorted_by_ids = adapter_ds.get_items_sorted_by_ids()
        self.assertTrue((StreamNdarrayAdapterDataStoreTestCase.items == items_sorted_by_ids).all())

    def test_save_items_sorted_by_ids(self):
        sqltable_ds = SQLiteTableDataStore(StreamNdarrayAdapterDataStoreTestCase.db_path,
                                           StreamNdarrayAdapterDataStoreTestCase.table_name, "ndarray")
        adapter_ds = StreamNdarrayAdapterDataStore(sqltable_ds, detect_final_shape_by_first_elem=True)

        adapter_ds.save_items_sorted_by_ids(StreamNdarrayAdapterDataStoreTestCase.items)

        with sqltable_ds:
            items_sorted_by_ids = sqltable_ds.get_items_sorted_by_ids()
            for arr1, arr2 in zip(items_sorted_by_ids, StreamNdarrayAdapterDataStoreTestCase.items):
                self.assertTrue((arr1 == arr2).all())

    def test_save_items_sorted_by_ids_particular_ids(self):
        sqltable_ds = SQLiteTableDataStore(StreamNdarrayAdapterDataStoreTestCase.db_path,
                                           StreamNdarrayAdapterDataStoreTestCase.table_name, "ndarray")
        adapter_ds = StreamNdarrayAdapterDataStore(sqltable_ds, detect_final_shape_by_first_elem=True)

        ids_sorted = np.arange(1, len(StreamNdarrayAdapterDataStoreTestCase.items) + 1) * 2
        adapter_ds.save_items_sorted_by_ids(StreamNdarrayAdapterDataStoreTestCase.items, ids_sorted)

        with sqltable_ds:
            items_sorted_by_ids = sqltable_ds.get_items_sorted_by_ids()
            for arr1, arr2 in zip(items_sorted_by_ids, StreamNdarrayAdapterDataStoreTestCase.items):
                self.assertTrue((arr1 == arr2).all())


if __name__ == '__main__':
    unittest.main()
