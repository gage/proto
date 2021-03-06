"""Auto-generated file, do not edit by hand. MN metadata"""
from phonenumbers import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_MN = PhoneMetadata(id='MN', country_code=976, international_prefix='001',
    general_desc=PhoneNumberDesc(national_number_pattern=u'[12]\d{7,9}|[57-9]\d{7}', possible_number_pattern=u'\d{6,10}'),
    fixed_line=PhoneNumberDesc(national_number_pattern=u'[12](?:1\d|2(?:[1-3]\d?|7\d)|3[2-8]\d{1,2}|4[2-68]\d{1,2}|5[1-4689]\d{1,2})\d{5}|(?:5[0568]|70)\d{6}', possible_number_pattern=u'\d{6,10}', example_number=u'70123456'),
    mobile=PhoneNumberDesc(national_number_pattern=u'(?:8[89]|9[15689])\d{6}', possible_number_pattern=u'\d{8}', example_number=u'88123456'),
    toll_free=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    premium_rate=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    shared_cost=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    personal_number=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    voip=PhoneNumberDesc(national_number_pattern=u'7[569]\d{6}', possible_number_pattern=u'\d{8}', example_number=u'75123456'),
    pager=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    uan=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    no_international_dialling=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    national_prefix=u'0',
    national_prefix_for_parsing=u'0',
    number_format=[NumberFormat(pattern='([12]\d)(\d{2})(\d{4})', format=u'\\1 \\2 \\3', leading_digits_pattern=['[12]1'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='([12]2\d)(\d{5,6})', format=u'\\1 \\2', leading_digits_pattern=['[12]2[1-3]'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='([12]\d{3})(\d{5})', format=u'\\1 \\2', leading_digits_pattern=['[12](?:27|[3-5])', '[12](?:27|[3-5]\d)2'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(\d{4})(\d{4})', format=u'\\1 \\2', leading_digits_pattern=['[57-9]'], national_prefix_formatting_rule=u'\\1'),
        NumberFormat(pattern='([12]\d{4})(\d{4,5})', format=u'\\1 \\2', leading_digits_pattern=['[12](?:27|[3-5])', '[12](?:27|[3-5]\d)[4-9]'], national_prefix_formatting_rule=u'0\\1')])
