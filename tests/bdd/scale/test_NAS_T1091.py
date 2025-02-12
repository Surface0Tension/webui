# coding=utf-8
"""SCALE UI: feature tests."""

import time
from function import(
    wait_on_element,
    is_element_present,
    wait_for_attribute_value,
    wait_on_element_disappear,
    attribute_value_exist,
)
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('features/NAS-T1091.feature', 'Add a home directory to a user')
def test_add_a_home_directory_to_a_user():
    """Add a home directory to a user."""


@given('the browser is open, the FreeNAS URL and logged in')
def the_browser_is_open_the_freenas_url_and_logged_in(driver, nas_ip, root_password):
    """the browser is open, the FreeNAS URL and logged in."""
    if nas_ip not in driver.current_url:
        driver.get(f"http://{nas_ip}")
        assert wait_on_element(driver, 10, '//input[@data-placeholder="Username"]')
    if not is_element_present(driver, '//mat-list-item[@ix-auto="option__Dashboard"]'):
        assert wait_on_element(driver, 10, '//input[@data-placeholder="Username"]')
        driver.find_element_by_xpath('//input[@data-placeholder="Username"]').clear()
        driver.find_element_by_xpath('//input[@data-placeholder="Username"]').send_keys('root')
        driver.find_element_by_xpath('//input[@data-placeholder="Password"]').clear()
        driver.find_element_by_xpath('//input[@data-placeholder="Password"]').send_keys(root_password)
        assert wait_on_element(driver, 5, '//button[@name="signin_button"]')
        driver.find_element_by_xpath('//button[@name="signin_button"]').click()
    else:
        driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Dashboard"]').click()


@when('you should be on the dashboard, click on the Accounts on the side menu, click on Users')
def you_should_be_on_the_dashboard_click_on_the_accounts_on_the_side_menu_click_on_users(driver):
    """you should be on the dashboard, click on the Accounts on the side menu, click on Users."""
    assert wait_on_element(driver, 10, '//span[contains(.,"Dashboard")]')
    assert wait_on_element(driver, 10, '//mat-list-item[@ix-auto="option__Dashboard"]', 'clickable')
    driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Dashboard"]').click()
    time.sleep(2)
    """click on the Credentials on the side menu, click on Local Users."""
    assert wait_on_element(driver, 10, '//mat-list-item[@ix-auto="option__Credentials"]', 'clickable')
    driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Credentials"]').click()
    time.sleep(2)
    assert wait_on_element(driver, 10, '//*[contains(@class,"lidein-nav-md")]//mat-list-item[@ix-auto="option__Local Users"]', 'clickable')
    driver.find_element_by_xpath('//*[contains(@class,"lidein-nav-md")]//mat-list-item[@ix-auto="option__Local Users"]').click()
    
    
@when('the Users page should open, expand the user and click the edit button')
def the_users_page_should_open_expand_the_user_and_click_the_edit_button(driver):
    """the Users page should open, expand the user and click the edit button."""
    time.sleep(2)
    assert wait_on_element(driver, 7, '//div[contains(.,"Users")]')
    assert wait_on_element(driver, 10, '//tr[@ix-auto="expander__ericbsd"]/td', 'clickable')
    driver.find_element_by_xpath('//tr[@ix-auto="expander__ericbsd"]/td').click()
    time.sleep(1)
    assert wait_on_element(driver, 10, '//button[@ix-auto="button__EDIT_ericbsd"]', 'clickable')
    driver.find_element_by_xpath('//button[@ix-auto="button__EDIT_ericbsd"]').click()


@then('the User Edit Page should open, change the path of the users Home Directory')
def the_user_edit_page_should_open_change_the_path_of_the_users_home_directory(driver):
    """the User Edit Page should open, change the path of the users Home Directory."""
    assert wait_on_element(driver, 10, '//h3[contains(.,"Edit User")]')
    time.sleep(4)
    assert wait_on_element(driver, 2, '//input[@ix-auto="input__home"]')
    driver.find_element_by_xpath('//input[@ix-auto="input__home"]').clear()
    driver.find_element_by_xpath('//input[@ix-auto="input__home"]').send_keys('/mnt/tank/ericbsd')


@then('click save and changes should be saved, the drop-down details pane should show the home directory has changed')
def click_save_and_changes_should_be_saved_the_dropdown_details_pane_should_show_the_home_directory_has_changed(driver):
    """click save and changes should be saved, the drop-down details pane should show the home directory has changed."""
    assert wait_on_element(driver, 2, '//button[@ix-auto="button__SAVE"]')
    driver.find_element_by_xpath('//button[@ix-auto="button__SAVE"]').click()
    assert wait_on_element_disappear(driver, 20, '//h6[contains(.,"Please wait")]')
    assert wait_on_element(driver, 2, '//div[contains(.,"Users")]')
    time.sleep(6)
    assert wait_on_element(driver, 7, '//div[contains(.,"Users")]')
    assert wait_on_element(driver, 10, '//tr[@ix-auto="expander__ericbsd"]/td', 'clickable')
    driver.find_element_by_xpath('//tr[@ix-auto="expander__ericbsd"]/td').click()
    #driver.find_element_by_xpath('//h4[contains(.,"/nonexistent")]') is False
    assert wait_on_element(driver, 10, '//h4[contains(.,"/nonexistent")]') is False
    ## return to dashboard
    time.sleep(1)
    assert wait_on_element(driver, 10, '//mat-list-item[@ix-auto="option__Dashboard"]', 'clickable')
    driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Dashboard"]').click()
    time.sleep(1)

