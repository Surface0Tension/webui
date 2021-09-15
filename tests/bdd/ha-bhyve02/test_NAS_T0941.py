# coding=utf-8
"""High Availability (tn-bhyve03) feature tests."""

import time
from function import (
    wait_on_element,
    is_element_present,
    wait_on_element_disappear,
    attribute_value_exist
)
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers
)


@scenario('features/NAS-T941.feature', 'Create a new dataset with the LDAP user and group.')
def test_create_a_new_dataset_with_the_ldap_user_and_group(driver):
    """Create a new dataset with the LDAP user and group.."""


@given(parsers.parse('The browser is open navigate to "{nas_url}"'))
def the_browser_is_open_navigate_to_nas_url(driver, nas_url):
    """The browser is open navigate to "{nas_url}"."""
    if nas_url not in driver.current_url:
        driver.get(f"http://{nas_url}/ui/sessions/signin")
        time.sleep(1)


@when(parsers.parse('If login page appear enter "{user}" and "{password}"'))
def if_login_page_appear_enter_root_and_password(driver, user, password):
    """If login page appear enter "user" and "password"."""
    if not is_element_present(driver, '//mat-list-item[@ix-auto="option__Dashboard"]'):
        assert wait_on_element(driver, 10, '//input[@placeholder="Username"]')
        driver.find_element_by_xpath('//input[@placeholder="Username"]').clear()
        driver.find_element_by_xpath('//input[@placeholder="Username"]').send_keys(user)
        driver.find_element_by_xpath('//input[@placeholder="Password"]').clear()
        driver.find_element_by_xpath('//input[@placeholder="Password"]').send_keys(password)
        assert wait_on_element(driver, 4, '//button[@name="signin_button"]')
        driver.find_element_by_xpath('//button[@name="signin_button"]').click()
    else:
        element = driver.find_element_by_xpath('//span[contains(.,"root")]')
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(0.5)
        driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Dashboard"]').click()


@then('You should see the dashboard and "System Information"')
def you_should_see_the_dashboard_and_system_information(driver):
    """You should see the dashboard and "System Information"."""
    assert wait_on_element(driver, 7, '//span[contains(.,"System Information")]')


@then('Go to Storage click Pools')
def go_to_storage_click_pools(driver):
    """Go to Storage click Pools."""
    driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Storage"]').click()
    assert wait_on_element(driver, 7, '//mat-list-item[@ix-auto="option__Pools"]', 'clickable')
    driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Pools"]').click()


@then('The Pools page should open')
def the_pools_page_should_open(driver):
    """The Pools page should open."""
    assert wait_on_element(driver, 7, '//div[contains(.,"Pools")]')


@then('Click on the dozer 3 dots button, select Add Dataset')
def click_on_the_dozer_3_dots_button_select_add_dataset(driver):
    """Click on the dozer 3 dots button, select Add Dataset."""
    assert wait_on_element(driver, 7, '//mat-icon[@id="actions_menu_button__dozer"]', 'clickable')
    driver.find_element_by_xpath('//mat-icon[@id="actions_menu_button__dozer"]').click()
    assert wait_on_element(driver, 7, '//button[@ix-auto="action__dozer_Add Dataset"]', 'clickable')
    driver.find_element_by_xpath('//button[@ix-auto="action__dozer_Add Dataset"]').click()


@then('The Add Dataset Name and Options page should open')
def the_add_dataset_name_and_options_page_should_open(driver):
    """The Add Dataset Name and Options page should open."""
    assert wait_on_element(driver, 7, '//h4[contains(.,"Name and Options")]')


@then(parsers.parse('Input dataset name "{dataset_name}" and click save'))
def input_dataset_name_my_ldap_dataset_and_click_save(driver, dataset_name):
    """Input dataset name "my_ldap_dataset" and click save."""
    assert wait_on_element(driver, 7, '//input[@ix-auto="input__Name"]', 'clickable')
    driver.find_element_by_xpath('//input[@ix-auto="input__Name"]').clear()
    driver.find_element_by_xpath('//input[@ix-auto="input__Name"]').send_keys(dataset_name)
    driver.find_element_by_xpath('//button[@ix-auto="button__SUBMIT"]').click()


@then(parsers.parse('"{dataset_name}" should be created'))
def my_ldap_dataset_should_be_created(driver, dataset_name):
    """"my_ldap_dataset" should be created."""
    assert wait_on_element_disappear(driver, 20, '//h6[contains(.,"Please wait")]')
    assert wait_on_element(driver, 10, f'//span[contains(.,"{dataset_name}")]')


@then(parsers.parse('Click on "{dataset_name}" 3 dots button, select Edit Permissions'))
def click_on_my_ldap_dataset_3_dots_button_select_edit_permissions(driver, dataset_name):
    """Click on "my_ldap_dataset" 3 dots button, select Edit Permissions."""
    assert wait_on_element(driver, 7, f'//mat-icon[@ix-auto="options__{dataset_name}"]', 'clickable')
    driver.find_element_by_xpath(f'//mat-icon[@id="actions_menu_button__{dataset_name}"]').click()
    assert wait_on_element(driver, 7, f'//button[@ix-auto="action__{dataset_name}_Edit Permissions"]', 'clickable')
    driver.find_element_by_xpath(f'//button[@ix-auto="action__{dataset_name}_Edit Permissions"]').click()


@then('The Edit Permissions page should open')
def the_edit_permissions_page_should_open(driver):
    """The Edit Permissions page should open."""
    assert wait_on_element(driver, 7, '//h4[contains(.,"Dataset Path")]')


@then(parsers.parse('Select "{ldap_user}" for User, check the Apply User then select "{ldap_group}" for Group name, check the Apply Group'))
def select_user_check_the_apply_user_then_select_group_name_check_the_apply_group(driver, ldap_user, ldap_group):
    """Select "ldap_user" for User, check the Apply User then select "ldap_group" for Group name, check the Apply Group."""
    assert wait_on_element(driver, 7, '//mat-checkbox[@ix-auto="checkbox__Apply User"]/label/div', 'clickable')
    driver.find_element_by_xpath('//mat-checkbox[@ix-auto="checkbox__Apply User"]/label/div').click()
    assert wait_on_element(driver, 7, '//input[@placeholder="User"]', 'clickable')
    driver.find_element_by_xpath('//input[@placeholder="User"]').clear()
    driver.find_element_by_xpath('//input[@placeholder="User"]').send_keys(ldap_user)
    assert wait_on_element(driver, 7, '//mat-checkbox[@ix-auto="checkbox__Apply Group"]/label/div', 'clickable')
    driver.find_element_by_xpath('//mat-checkbox[@ix-auto="checkbox__Apply Group"]/label/div').click()
    assert wait_on_element(driver, 7, '//input[@placeholder="Group"]', 'clickable')
    driver.find_element_by_xpath('//input[@placeholder="Group"]').clear()
    driver.find_element_by_xpath('//input[@placeholder="Group"]').send_keys(ldap_group)


@then('Click the Save button, should be return to pool page')
def click_the_save_button_should_be_return_to_pool_page(driver):
    """Click the Save button, should be return to pool page."""
    assert wait_on_element(driver, 7, '//button[@ix-auto="button__SAVE"]', 'clickable')
    driver.find_element_by_xpath('//button[@ix-auto="button__SAVE"]').click()
    assert wait_on_element_disappear(driver, 20, '//h6[contains(.,"Please wait")]')
    assert wait_on_element(driver, 7, '//mat-panel-title[contains(.,"dozer")]')
    driver.find_element_by_xpath('//td[@ix-auto="value__dozer_name"]')


@then(parsers.parse('Verify that user and group name is "{ldap_user}"'))
def verify_that_user_and_group_name(driver, ldap_user):
    """Verify that user and group name is "ldap_user"."""
    assert wait_on_element(driver, 7, '//input[@placeholder="User"]')
    assert attribute_value_exist(driver, '//input[@placeholder="User"]', 'value', ldap_user)
    assert attribute_value_exist(driver, '//input[@placeholder="Group"]', 'value', ldap_user)