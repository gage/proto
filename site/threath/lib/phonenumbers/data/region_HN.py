"""Auto-generated file, do not edit by hand. HN metadata"""
from phonenumbers import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_HN = PhoneMetadata(id='HN', country_code=504, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern=u'[237-9]\d{7}', possible_number_pattern=u'\d{8}'),
    fixed_line=PhoneNumberDesc(national_number_pattern=u'2(?:2(?:0[019]|1[1-36]|[23]\d|4[056]|5[57]|9[01])|4(?:2|3-59]|3[13-689]|4[0-68]|5[1-35])|5(?:4[3-5]|5\d|6[56]|74)|6(?:4[0-378]|[56]\d|[78][0-8]|9[01])|7(?:6[46-9]|7[02-9]|8[34])|8(?:79|8[0-35789]|9[1-57-9]))\d{4}', possible_number_pattern=u'\d{8}', example_number=u'22123456'),
    mobile=PhoneNumberDesc(national_number_pattern=u'[37-9]\d{7}', possible_number_pattern=u'\d{8}', example_number=u'91234567'),
    toll_free=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    premium_rate=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    shared_cost=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    personal_number=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    voip=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    pager=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    uan=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    no_international_dialling=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    number_format=[NumberFormat(pattern='(\d{4})(\d{4})', format=u'\\1-\\2')])
