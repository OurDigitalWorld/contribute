
import os
from os.path import splitext
from django.core.mail import send_mail
from contribute.settings import PROJECT_MEDIA_ROOT, VITA_EMAIL
from CrowdSourcing.customlog import log_request
from DataEntry.sql import sql_call, sql_update
from DataEntry.models import Record, RecordObject

# TODO  unblock copyfile about line 170


def commit(record_id, group_id):
    if record_id:
        agency_id = 0
        bln_agency_save_original = False
        site_display_public = 0
        bln_site_display_public = False
        group_list = group_id.split('.')
        int_group_id = group_list[1]
        agency_id_sql = ("SELECT R.agency_id "
                      "FROM groups G "
                      "JOIN records R ON G.record_id = R.id  "
                      "WHERE G.id='{}'").format(int_group_id)
        agency_id_set = sql_call(agency_id_sql, 'vita')
        for a_id in agency_id_set:
            agency_id = a_id.agency_id
        # print('agency_id: ', agency_id)
        agency_sql = ("SELECT agency_image_file_path, agency_image_url, feedback_email, "
                      "agency_save_original, site_path "
                      "FROM agencies A "
                      "JOIN sites S ON A.preferred_site_id = S.id "
                      "WHERE A.id = '{}'").format(agency_id)
        agency_set = sql_call(agency_sql, 'vita')
        for agency in agency_set:
            agency_image_file_path = agency.agency_image_file_path
            agency_image_url = agency.agency_image_url
            feedback_email = agency.feedback_email
            site_path  = agency.site_path
            agency_save_original = agency.agency_save_original
            if agency_save_original == '1':
                bln_agency_save_original = True
        # print('agency_image_file_path: ', agency_image_file_path)
        prediction_sql = ("SELECT AP.*, A.agency_image_file_path, A.agency_image_url "
                          "FROM agencypredictions AP "
                          "JOIN agencies A ON AP.agency_id = A.id "
                          "WHERE AP.agency_id = '{}'").format(agency_id)
        prediction_set = sql_call(prediction_sql, 'vita')
        site_sql = ("SELECT site_id, site_path "
                    "FROM sitesetup "
                    "JOIN sites ON sitesetup.site_id = sites.id "
                    "WHERE afield ILIKE 'ConGroupID' "
                    "AND avalue ILIKE '{}'").format(int_group_id)
        site_set = sql_call(site_sql, 'vita')
        for site in site_set:
            site_id = site.site_id
            site_path = site.site_path
        # print('site_id: ', site_id)
        # print('site_path: ', site_path)
        site_display_sql = ("SELECT avalue "
                            "FROM sitesetup "
                            "WHERE afield ILIKE 'ConPublicDisplay' "
                            "AND site_id = '{}'").format(site_id)
        site_display_set = sql_call(site_display_sql, 'vita')
        for site in site_display_set:
            site_display_public = site.avalue
        if site_display_public == 0:
            site_prototype_sql = ("SELECT avalue "
                                  "FROM sites AS S "
                                  "JOIN sitesetup AS SS ON S.prototype_site_id = SS.site_id "
                                  "AND SS.afield = 'ConPublicDisplay' "
                                  "WHERE S.id = '{}'").format(site_id)
            site_display_set = sql_call(site_prototype_sql, 'vita')
            for site in site_display_set:
                site_display_public = site.avalue
                # print('avalue: ', site.avalue)
        # print('site_display_public: ', site_display_public)
        if site_display_public == 1:
            bln_site_display_public = True
        vita_record_id, record_set = create_record(record_id, site_display_public, agency_id)
        if vita_record_id > 0:
            comp_thumb = create_record_objects(record_id, vita_record_id, agency_id, prediction_set)
        # TODO eventually add geography
        group_sql = ("INSERT INTO recordgroups (record_id, group_id) "
                     "VALUES ('{}', '{}')").format(vita_record_id, int_group_id)
        # print(group_sql)
        sql_update(group_sql)
        reorder_objects(vita_record_id)
        comp_url = update_comp_fields(vita_record_id, comp_thumb, site_path)
        if feedback_email:
            subject = "A Record has been contributed to your VITA agency"
            message = ('A record has been added to your site via the Contribution module.  '
                       'You can confirm the contents by logging in at https://data.vitatoolkit.ca/'
                       ' and checking Record ID: {}').format(vita_record_id)
            send_mail(subject, message, VITA_EMAIL, [feedback_email])
        return comp_url, comp_thumb


def create_record(record_id, site_display_public, agency_id):
    record_set = Record.objects.filter(pk=record_id)
    # print(record_1_set)
    vita_record_id = 0
    for record in record_set:
        title = double_apostrophe(record.title)
        description = double_apostrophe(record.description)
        record_contributor = double_apostrophe(record.contributor)
        record_contributor_email = record.contributor_email
        record_contributor_name_permission = record.contributor_name_permission
        fulltext = double_apostrophe(record.full_text)
        image_file_name = record.filename
        # print(image_file_name)
        media_type_id = get_media_type(image_file_name)

        sql_1 = "INSERT INTO records (title, comp_title"
        sql_2 = " VALUES ('{}', '{}'".format(title, title)

        if description:
            sql_1 += ', description, comp_description'
            sql_2 += ", '{}', '{}'".format(description, description)
        if record_contributor:
            sql_1 += ', record_contributor'
            sql_2 += ", '{}'".format(record_contributor)
        if record_contributor_email:
            sql_1 += ', record_contributor_email'
            sql_2 += ", '{}'".format(record_contributor_email)
        if record_contributor_name_permission:
            sql_1 += ',record_contributor_name_permission'
            sql_2 += ", '{}'".format(record_contributor_name_permission)
        if fulltext:
            sql_1 += ', fulltext'
            sql_2 += ", '{}'".format(fulltext)
        if fulltext:
            sql_1 += ', media_type_id'
            sql_2 += ", '{}'".format(media_type_id)
        if site_display_public:
            sql_1 += ', public_display'
            sql_2 += ", '{}'".format(site_display_public)
        if agency_id:
            sql_1 += ', agency_id'
            sql_2 += ", '{}'".format(agency_id)
        sql_1 += ", date_added, date_modified, contributed, relator_id)"
        sql_2 += ", CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '1', '0') RETURNING id AS newid;"
        record_insert_sql = sql_1 + sql_2
        # print(record_insert_sql)
        vita_record_set = sql_call(record_insert_sql, 'vita')
        for new_record in vita_record_set:
            vita_record_id = new_record.newid
        # print(vita_record_id)
        # print('type: ', type(vita_record_id))
    return vita_record_id, record_set


def create_record_objects(record_id, vita_record_id, agency_id, prediction_set):
    comp_thumb = ''
    for prediction in prediction_set:
        agency_image_file_url = prediction.agency_image_url
    record_object_set = RecordObject.objects.filter(record_id=record_id)
    for ro_object in record_object_set:
        display_link = '1'
        if ro_object.record_object_category_id == 4:
            display_link = '0'
        object_order = int(ro_object.record_object_category_id) + 1
        if ro_object.full_text:
            fulltext = "'{}'".format(double_apostrophe(ro_object.full_text))
        else:
            fulltext = 'NULL'
        contribute_file_type = ro_object.file_type
        vita_file_name, vita_file_path = get_vita_file_name(agency_id, vita_record_id, ro_object.file_name, ro_object.record_object_category_id, prediction_set)
        if contribute_file_type == 'JPEG2000':
            vita_file_name = vita_file_name.replace('.jpg', '.jp2')
            vita_file_path = vita_file_path.replace('.jpg', '.jp2')

        ro_sql = (("INSERT INTO recordobjects (record_id, file_name, file_size, "
                  "file_type, object_height, object_width, original_file_name, "
                  "record_object_category_id_2, object_order, display_link, "
                  "url_exists, fulltext) "
                  "Values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '1', {})").format
                  (vita_record_id, vita_file_name, ro_object.file_size, ro_object.file_type,
                          ro_object.object_height, ro_object.object_width, ro_object.original_file_name,
                          ro_object.record_object_category_id, object_order, display_link, fulltext))
        # print(ro_sql)
        sql_update(ro_sql)
        vita_file_path_escaped = escape_backslash(vita_file_path).strip()
        # log_request("vita_file_path_escaped", vita_file_path_escaped)
        partner_path = escape_backslash(get_vita_setup_field('PartnerPath').strip())
        # log_request("partner_path", partner_path)
        web_services_partner_path = escape_backslash(get_vita_setup_field('WebServicesPartnerPath').strip())
        # log_request("web_services_partner_path", web_services_partner_path)
        target_path = vita_file_path_escaped.replace(partner_path, web_services_partner_path)
        # log_request("target_path XXXX", target_path)
        target_path = target_path.replace("XXXX", "\\")
        target_path = target_path.replace("YYYY", ":")
        # log_request('target_path after X: ', target_path)
        # log_request('ro.file_name: ', ro_object.file_name)
        if ro_object.record_object_category_id == 0:
            comp_thumb = '{}{}'.format(agency_image_file_url, vita_file_name)
        copy_file(ro_object.file_name, target_path)
    return comp_thumb


def get_vita_file_name(agency_id, record_id, con_file_name, record_object_category_id, prediction_set):
    vita_file_name = ''
    location = ''
    extension = splitext(con_file_name)
    original_extension = extension[1].lower()
    for prediction in prediction_set:
        file_prefix = prediction.fileprefix.strip()
        zero_pad_record_id = f"{record_id:0>9}"
        size0 = prediction.size0
        size1 = prediction.size1
        size2 = prediction.size2
        location0 = prediction.location0
        location1 = prediction.location1
        location2 = prediction.location2
        location4 = prediction.location4
        agency_image_file_path = prediction.agency_image_file_path
    if record_object_category_id == 0:
        vita_file_name = '{}{}{}'.format(file_prefix, zero_pad_record_id, size0)
        if location0:
            location = location0
    if record_object_category_id == 1:
        vita_file_name = '{}{}{}'.format(file_prefix, zero_pad_record_id, size1)
        if location1:
            location = location1
    if record_object_category_id == 2:
        vita_file_name = '{}{}{}'.format(file_prefix, zero_pad_record_id, size2)
        if location2:
            location = location2
    if record_object_category_id == 4:
        vita_file_name = '{}{}o{}'.format(file_prefix, zero_pad_record_id, original_extension)
        if location4:
            location = location4
    vita_file_path = '{}{}\\{}'.format(agency_image_file_path, location, vita_file_name)
    vita_file_path = vita_file_path.replace('\\\\', '\\')
    # log_request("vita_file_path: ", vita_file_path)
    return vita_file_name.strip(), vita_file_path.strip()


def get_media_type(image_file):
    image_list = ['JPEG', 'JPG', 'PNG', 'GIF', 'WEBP',
                  'TIF', 'TIFF', 'JP2', 'HEIC', 'BMP']
    text_list = ['DOC', 'DOCX', 'TXT', 'RTF', 'PDF']
    extension = splitext(image_file)
    upper_extension = extension[1].upper()
    if upper_extension in image_list:
        media_type_id = 1
    elif upper_extension in text_list:
        media_type_id = 2
    else:
        media_type_id = ''
    return media_type_id


def double_apostrophe(string):
    if string:
        if "'" in string:
            string = string.replace("'", "''")
    return string


def escape_backslash(string):
    if "\\" in string:
        string = string.replace("\\", "XXXX")
    if ":" in string:
        string = string.replace(":", "YYYY")
    return string


def get_vita_setup_field(field):
    field_value = ''
    setup_sql = "SELECT avalue FROM setup WHERE afield ILIKE '{}'".format(field)
    # log_request("setup_sql:", setup_sql)
    setup_set = sql_call(setup_sql, 'vita')
    for field in setup_set:
        field_value = field.avalue
    # log_request("field_value: ", field_value)
    return field_value


def copy_file(file_name, destination):
    root = PROJECT_MEDIA_ROOT.replace('/','\\')
    copy_plan = "copy %s%s %s" % (root, file_name, destination)
    # log_request("commit copyplan: ", copy_plan)
    os.popen(copy_plan)
    return 'ok'


def reorder_objects(vita_record_id):
    order_sql = ("SELECT id FROM recordobjects "
                 "WHERE record_id = '{}' "
                 "ORDER BY object_order").format(vita_record_id)
    # print(order_sql)
    order_set = sql_call(order_sql, 'vita')
    counter = 0
    # print(order_set)
    # print(counter)
    for record in order_set:
        counter += 1
        update_order_sql = ("UPDATE recordobjects "
                            "SET object_order='{}' "
                            "WHERE id='{}'").format(counter, record.id)
        # print(update_order_sql)
        sql_update(update_order_sql)


def update_comp_fields(vita_record_id, comp_thumb, site_path):
    comp_url = '{}{}/data'.format(site_path, vita_record_id)
    update_comp_sql = ("UPDATE records "
                       "SET comp_thumb='{}', comp_url='{}' "
                       "WHERE id='{}'").format(comp_thumb, comp_url, vita_record_id)
    sql_update(update_comp_sql)
    return comp_url
