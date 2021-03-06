"""Auto-generated file, do not edit by hand. BD metadata"""
from phonenumbers import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_BD = PhoneMetadata(id='BD', country_code=880, international_prefix='00[12]?',
    general_desc=PhoneNumberDesc(national_number_pattern=u'[2-79]\d{5,9}|1\d{9}|8[0-7]\d{4,8}', possible_number_pattern=u'\d{6,10}'),
    fixed_line=PhoneNumberDesc(national_number_pattern=u'2(?:7\d1|8(?:[026]1|[1379][1-5]|8[1-8])|9(?:0[0-2]|1[1-4]|3[3-5]|5[56]|6[67]|71|8[078]))\d{4}|3(?:[6-8]1|(?:0[23]|[25][12]|82|416)\d|(?:31|12?[5-7])\d{2})\d{3}|4(?:(?:02|[49]6|[68]1)|(?:0[13]|21\d?|[23]2|[457][12]|6[28])\d|(?:23|[39]1)\d{2}|1\d{3})\d{3}|5(?:(?:[457-9]1|62)|(?:1\d?|2[12]|3[1-3]|52)\d|61{2})|6(?:[45]1|(?:11|2[15]|[39]1)\d|(?:[06-8]1|62)\d{2})|7(?:(?:32|91)|(?:02|31|[67][12])\d|[458]1\d{2}|21\d{3})\d{3}|8(?:(?:4[12]|[5-7]2|1\d?)|(?:0|3[12]|[5-7]1|217)\d)\d{4}|9(?:[35]1|(?:[024]2|81)\d|(?:1|[24]1)\d{2})\d{3}', possible_number_pattern=u'\d{6,9}', example_number=u'27111234'),
    mobile=PhoneNumberDesc(national_number_pattern=u'(?:1[13-9]\d|(?:3[78]|44)[02-9]|6(?:44|6[02-9]))\d{7}', possible_number_pattern=u'\d{10}', example_number=u'1812345678'),
    toll_free=PhoneNumberDesc(national_number_pattern=u'80[03]\d{7}', possible_number_pattern=u'\d{10}', example_number=u'8001234567'),
    premium_rate=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    shared_cost=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    personal_number=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    voip=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    pager=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    uan=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    no_international_dialling=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    preferred_international_prefix=u'00',
    national_prefix=u'0',
    national_prefix_for_parsing=u'0',
    number_format=[NumberFormat(pattern='(2)(\d{7})', format=u'\\1 \\2', leading_digits_pattern=['2'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(\d{2})(\d{4,6})', format=u'\\1 \\2', leading_digits_pattern=['[3-79]1'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(\d{3})(\d{3,7})', format=u'\\1 \\2', leading_digits_pattern=['[3-79][2-9]|8'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(\d{4})(\d{6})', format=u'\\1 \\2', leading_digits_pattern=['1'], national_prefix_formatting_rule=u'0\\1')])
