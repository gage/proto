"""Auto-generated file, do not edit by hand. AE metadata"""
from phonenumbers import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_AE = PhoneMetadata(id='AE', country_code=971, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern=u'[2-79]\d{7,8}|800\d{2,9}', possible_number_pattern=u'\d{5,12}'),
    fixed_line=PhoneNumberDesc(national_number_pattern=u'(?:[2-4679][2-8]\d|600[25])\d{5}', possible_number_pattern=u'\d{7,9}', example_number=u'22345678'),
    mobile=PhoneNumberDesc(national_number_pattern=u'5[056]\d{7}', possible_number_pattern=u'\d{9}', example_number=u'501234567'),
    toll_free=PhoneNumberDesc(national_number_pattern=u'400\d{6}|800\d{2,9}', possible_number_pattern=u'\d{5,12}', example_number=u'800123456'),
    premium_rate=PhoneNumberDesc(national_number_pattern=u'900[02]\d{5}', possible_number_pattern=u'\d{9}', example_number=u'900234567'),
    shared_cost=PhoneNumberDesc(national_number_pattern=u'700[05]\d{5}', possible_number_pattern=u'\d{9}', example_number=u'700012345'),
    personal_number=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    voip=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    pager=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    uan=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    no_international_dialling=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    national_prefix=u'0',
    national_prefix_for_parsing=u'0',
    number_format=[NumberFormat(pattern='([2-4679])(\d{3})(\d{4})', format=u'\\1 \\2 \\3', leading_digits_pattern=['[2-4679][2-8]'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(5[056])(\d{3})(\d{4})', format=u'\\1 \\2 \\3', leading_digits_pattern=['5'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='([4679]00)(\d)(\d{5})', format=u'\\1 \\2 \\3', leading_digits_pattern=['[4679]0'], national_prefix_formatting_rule=u'\\1'),
        NumberFormat(pattern='(800)(\d{2,9})', format=u'\\1 \\2', leading_digits_pattern=['8'], national_prefix_formatting_rule=u'\\1')])
