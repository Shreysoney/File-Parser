import parse
import pytest
from validate import FileModel

def test_validate_valid_file_name():
    """
    GIVEN a FileModel Class to validate file-name by extracting 
    file-year and file-month.
    WHEN valid data file-name is passed
    THEN check that the validation is successful.
    """
    validated_file= FileModel(file_name="expedia_report_monthly_march_2018.xlsx")
    validated_file.give_month_year("expedia_report_monthly_march_2018.xlsx")
    assert validated_file.file_name=="expedia_report_monthly_march_2018.xlsx"
    assert FileModel.file_month==3
    assert FileModel.file_year==2018
    Calls_Offered,Abandon_after_30s,FCR,DSAT,CSAT=parse.parsing_worksheet1(validated_file.file_name,FileModel.file_month,FileModel.file_year)
    Promoters,Passives,Dectractors=parse.parsing_worksheet2(validated_file.file_name,FileModel.file_month,FileModel.file_year)
    assert Calls_Offered==22343
    assert Abandon_after_30s== 3.05
    assert FCR == 86.0
    assert DSAT == 18.0
    assert CSAT == 74.4
    assert Promoters == 'good'
    assert Passives == 'bad'
    assert Dectractors == 'bad' 

def test_validate_valid_file_name_tab_missing():
    """
    GIVEN a FileModel Class to validate file-name by extracting file-year and file-month
    and check if worksheets is present or not using parsing_worksheet1 function.
    WHEN valid data file-name is passed but the file doesn't contain the required Worksheet Tab.
    THEN check that the validation is successful by raising KeyError.
    """
    validated_file= FileModel(file_name="january_2019.xlsx")
    validated_file.give_month_year("january_2019.xlsx")
    assert validated_file.file_name=="january_2019.xlsx"
    assert FileModel.file_month==1
    assert FileModel.file_year==2019
    with pytest.raises(KeyError):
        parse.parsing_worksheet1(validated_file.file_name,FileModel.file_month,FileModel.file_year)


def test_validate_invalid_file_name_file_month():
    """
    GIVEN a FileModel Class to validate file-name by extracting file-year and file-month
    WHEN invalid data file-name is passed containg file-month but not file-year.
    THEN check that the validation is successful by raising ValueError.
    """
    with pytest.raises(ValueError):
        validated_file= FileModel(file_name="Shrey_expedition_re_january_142.xlsx")

def test_validate_invalid_file_name_with_year():
    """
    GIVEN a FileModel Class to validate file-name by extracting file-year and file-month
    WHEN invalid data file-name is passed containg file-year but not file-month.
    THEN check that the validation is successful by raising ValueError.
    """
    with pytest.raises(ValueError):
        validated_file= FileModel(file_name="Shrey_expedition_re_jany_2019.xlsx")

def test_validate_invalid_file_name_type_year_():
    """
    GIVEN a FileModel Class to validate file-name by extracting file-year and file-month
    WHEN invalid data file-name is passed containg invalid file-month and file-year that 
    cannot be converted into integer.
    THEN check that the validation is successful by raising ValueError.
    """
    with pytest.raises(ValueError):
        validated_file= FileModel(file_name="Shrey_expedition_re_jany_20ab.xlsx")





    

    