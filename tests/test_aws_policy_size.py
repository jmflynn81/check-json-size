from src import aws_policy_size


def test_aws_policy_size():
    test_dict = aws_policy_size.get_json("tests/test_json_file.json")
    assert type(test_dict) is dict
    size = aws_policy_size.get_policy_size(test_dict)
    assert size == 72


def test_aws_policy_size_nested():
    test_dict = aws_policy_size.get_json("tests/test_json_file.json")
    assert type(test_dict) is dict
    size = aws_policy_size.get_policy_size(test_dict, ["Roles"])
    assert size == 62


def test_aws_policy_size_good():
    assert aws_policy_size.main(["tests/test_json_file.json"]) == 0



def test_aws_policy_size_good_with_start_key():
    assert aws_policy_size.main(["--max-size",
                                 "100",
                                 "--start-key",
                                 ".Roles."
                                 "tests/test_json_file.json"
                                ]) == 0


def test_aws_policy_size_good_specify_max_size():
    assert aws_policy_size.main(["--max-size",
                                 "100",
                                 "tests/test_json_file.json"
                                ]) == 0


def test_aws_policy_size_bad():
    assert aws_policy_size.main(["--max-size",
                                    "6",
                                    "tests/test_json_file.json"
                                ]) == 1


def test_aws_policy_size_bad_with_start_key():
    assert aws_policy_size.main(["--max-size",
                                 "6",
                                 "--start-key",
                                 ".Roles.",
                                 "tests/test_json_file.json"
                                ]) == 1
