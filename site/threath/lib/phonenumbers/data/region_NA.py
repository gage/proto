"""Auto-generated file, do not edit by hand. NA metadata"""
from phonenumbers import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_NA = PhoneMetadata(id='NA', country_code=264, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern=u'[68]\d{7,8}', possible_number_pattern=u'\d{8,9}'),
    fixed_line=PhoneNumberDesc(national_number_pattern=u'6(?:1(?:17|2(?:[0189]\d|[23-6]|7\d?)|3(?:2\d|3[378])|4[01]|69|7[014])|2(?:17|25|5(?:[0-36-8]|4\d?)|69|70)|3(?:17|2(?:[0237]\d?|[14-689])|34|6[29]|7[01]|81)|4(?:17|2(?:[012]|7?)|4(?:[06]|1\d)|5(?:[01357]|[25]\d?)|69|7[01])|5(?:17|2(?:[0459]|[23678]\d?)|69|7[01])|6(?:17|2(?:5|6\d?)|38|42|69|7[01])|7(?:17|2(?:[569]|[234]\d?)|3(?:0\d?|[13])|69|7[01]))\d{4}', possible_number_pattern=u'\d{8,9}', example_number=u'612012345'),
    mobile=PhoneNumberDesc(national_number_pattern=u'(?:60|8[125])\d{7}', possible_number_pattern=u'\d{9}', example_number=u'811234567'),
    toll_free=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    premium_rate=PhoneNumberDesc(national_number_pattern=u'8701\d{5}', possible_number_pattern=u'\d{9}', example_number=u'870123456'),
    shared_cost=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    personal_number=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    voip=PhoneNumberDesc(national_number_pattern=u'886\d{5}', possible_number_pattern=u'\d{8}', example_number=u'88612345'),
    pager=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    uan=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    no_international_dialling=PhoneNumberDesc(national_number_pattern=u'NA', possible_number_pattern=u'NA'),
    national_prefix=u'0',
    national_prefix_for_parsing=u'0',
    number_format=[NumberFormat(pattern='(8\d)(\d{3})(\d{4})', format=u'\\1 \\2 \\3', leading_digits_pattern=['8[125]'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(6\d)(\d{2,3})(\d{4})', format=u'\\1 \\2 \\3', leading_digits_pattern=['6'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(88)(\d{3})(\d{3})', format=u'\\1 \\2 \\3', leading_digits_pattern=['88'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(870)(\d{3})(\d{3})', format=u'\\1 \\2 \\3', leading_digits_pattern=['870'], national_prefix_formatting_rule=u'0\\1')])
