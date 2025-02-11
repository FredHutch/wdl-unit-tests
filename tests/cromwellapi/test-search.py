import pytest

search_result_each = [
    "end",
    "id",
    "metadataArchiveStatus",
    "name",
    "start",
    "status",
    "submission",
]


# Check that search results are a subset as number of keys
# can range from 4 to 7 depending on the item
def contains_sublist(list1, list2):
    return set(list2).issubset(set(list1))


# We need to not match on "query" here because CromwellApi.search
# changes the date depending on what day the query is run, leading
# to no match against the stored cassette
VCR_SEARCH_CONFIG = {
    "match_on": ["method", "scheme", "path"],
}


@pytest.mark.vcr(**VCR_SEARCH_CONFIG)
def test_search_no_results(cromwell_api):
    """Checking that search works with no results"""
    out = cromwell_api.search(days=-2)
    # There should not be any results for a query for jobs
    # started in the future
    assert out["totalResultsCount"] == 0
    assert out["results"] == []


@pytest.mark.vcr(**VCR_SEARCH_CONFIG)
def test_search_results(cromwell_api):
    """Checking that search works when there MIGHT be results"""
    out = cromwell_api.search(days=1)
    # There may or may not be results, we can't gaurantee it
    if out["totalResultsCount"] == 0:
        pytest.skip("no results for search, skipping tests")
    else:
        assert isinstance(out["totalResultsCount"], int)
        assert len(out["results"]) > 0
        for item in out["results"]:
            assert contains_sublist(search_result_each, list(item.keys()))
