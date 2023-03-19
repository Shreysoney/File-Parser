from app import Summary_Rolling_MoM,VOC_Rolling_MoM
def test_SRM():
    """
    GIVEN a Summary_Rolling_MoM Class to validate data
    WHEN valid data is passed To Database Table
    THEN check that the validation is successful .
    """
    new_obj=Summary_Rolling_MoM(Calls_Offered=16695,Abandon_after_30s=2.32,FCR=86.3,DSAT=13,CSAT=80)
    assert new_obj.Calls_Offered == 16695
    assert new_obj.Abandon_after_30s == 2.32
    assert new_obj.FCR== 86.3
    assert new_obj.DSAT == 13
    assert new_obj.CSAT == 80

def test_VOC():
    """
    GIVEN a VOC_Rolling_MoM Class to validate data
    WHEN valid data is passed To Database Table
    THEN check that the validation is successful .
    """
    new_obj=VOC_Rolling_MoM(Promoters="good",Passives="good",Dectractors="bad")
    assert new_obj.Passives == "good"
    assert new_obj.Promoters == "good"
    assert new_obj.Dectractors== "bad"
    