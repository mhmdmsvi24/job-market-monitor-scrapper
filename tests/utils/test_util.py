from jmms.utils import create_csv, create_dir

def test_init_csv():
    """ """
    create_csv("jobs", 5, ["title", "company", "location", "contract"])
