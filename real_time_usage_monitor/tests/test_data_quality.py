
import pandas as pd
from pathlib import Path

def test_requirements_exists():
    assert Path('requirements.txt').exists()

def test_unique_event_ids():
    path = Path('data/raw/events_sample.csv')
    if path.exists():
        df = pd.read_csv(path)
        assert df['event_id'].is_unique
