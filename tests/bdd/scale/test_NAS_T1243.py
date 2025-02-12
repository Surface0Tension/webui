# coding=utf-8
"""SCALE UI: feature tests."""

import time
from function import(
    wait_on_element,
    is_element_present,
    attribute_value_exist,
    wait_for_attribute_value,
    wait_on_element_disappear,
)
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('features/NAS-T1243.feature', 'Verify that changing an encryption key format to PASSPHRASE functions')
def test_verify_that_changing_an_encryption_key_format_to_passphrase_functions():
    """SCALE UI: Verify that changing an encryption key format to PASSPHRASE functions."""


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


@when('you are on the dashboard, click Storage on the side menu')
def you_are_on_the_dashboard_click_storage_on_the_side_menu(driver):
    """you are on the dashboard, click Storage on the side menu."""
    assert wait_on_element(driver, 10, '//span[contains(.,"Dashboard")]')
    assert wait_on_element(driver, 10, '//mat-list-item[@ix-auto="option__Dashboard"]', 'clickable')
    driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Dashboard"]').click()
    assert wait_on_element(driver, 10, '//h1[contains(.,"Dashboard")]')
    assert wait_on_element(driver, 10, '//mat-list-item[@ix-auto="option__Storage"]', 'clickable')
    driver.find_element_by_xpath('//mat-list-item[@ix-auto="option__Storage"]').click()


@then('the pools page appears click the three dots for the encrypted pool')
def the_pools_page_appears_click_the_three_dots_for_the_encrypted_pool(driver):
    """the pools page appears click the three dots for the encrypted pool."""
    assert wait_on_element(driver, 10, '//h1[contains(.,"Storage")]')
    assert wait_on_element(driver, 5, '//tr[contains(.,"encrypted_tank")]//mat-icon[text()="more_vert"]', 'clickable')
    driver.find_element_by_xpath('//tr[contains(.,"tank")]//mat-icon[text()="more_vert"]').click()


@then('click encryption Options')
def click_encryption_options(driver):
    """click encryption Options."""
    assert wait_on_element(driver, 4, '//button[normalize-space(text())="Encryption Options"]', 'clickable')
    driver.find_element_by_xpath('//button[normalize-space(text())="Encryption Options"]').click()  
    assert wait_on_element(driver, 10, '//h1[contains(.,"Edit Encryption Options")]')


@then('set key type to passphrase')
def set_key_type_to_passphrase(driver):
    """set key type to passphrase."""
    assert wait_on_element(driver, 5, '//mat-select[@ix-auto="select__Encryption Type"]')
    driver.find_element_by_xpath('//mat-select[@ix-auto="select__Encryption Type"]').click()
    assert wait_on_element(driver, 5, '//mat-option[@ix-auto="option__Encryption Type_Passphrase"]', 'clickable')
    driver.find_element_by_xpath('//mat-option[@ix-auto="option__Encryption Type_Passphrase"]').click()


@then('enter acbd1234 and 1234abcd and verify that an error shows')
def enter_acbd1234_and_1234abcd_and_verify_that_an_error_shows(driver):
    """enter acbd1234 and 1234abcd and verify that an error shows."""
    assert wait_on_element(driver, 5, '//input[@ix-auto="input__Passphrase"]', 'inputable')
    driver.find_element_by_xpath('//input[@ix-auto="input__Passphrase"]').clear()
    driver.find_element_by_xpath('//input[@ix-auto="input__Passphrase"]').send_keys("abcd1234")
    assert wait_on_element(driver, 5, '//input[@ix-auto="input__Confirm Passphrase"]', 'inputable')
    driver.find_element_by_xpath('//input[@ix-auto="input__Confirm Passphrase"]').clear()
    driver.find_element_by_xpath('//input[@ix-auto="input__Confirm Passphrase"]').send_keys("1234abcd")
    assert wait_on_element(driver, 10, '//mat-error[contains(.,"The passwords do not match.")]')


@then('enter abcd1234 for both fields and confirm and save')
def enter_abcd1234_for_both_fields_and_confirm_and_save(driver):
    """enter abcd1234 for both fields and confirm and save."""
    assert wait_on_element(driver, 5, '//input[@ix-auto="input__Confirm Passphrase"]', 'inputable')
    driver.find_element_by_xpath('//input[@ix-auto="input__Confirm Passphrase"]').clear()
    driver.find_element_by_xpath('//input[@ix-auto="input__Confirm Passphrase"]').send_keys("abcd1234")
    assert wait_on_element(driver, 10, '//mat-error[contains(.,"The passwords do not match.")]') is False
    
    assert wait_on_element(driver, 10, '//mat-checkbox[@ix-auto="checkbox__Confirm"]', 'clickable')
    driver.find_element_by_xpath('//mat-checkbox[@ix-auto="checkbox__Confirm"]').click()   
    assert wait_on_element(driver, 5, '//button[@ix-auto="button__SAVE"]', 'clickable')
    driver.find_element_by_xpath('//button[@ix-auto="button__SAVE"]').click()
    assert wait_on_element_disappear(driver, 20, '//h6[contains(.,"Please wait")]')

    assert wait_on_element(driver, 10, '//h1[contains(.,"Encryption Options Saved")]')
    assert wait_on_element(driver, 5, '//button[@ix-auto="button__CLOSE"]', 'clickable')
    driver.find_element_by_xpath('//button[@ix-auto="button__CLOSE"]').click()


@then('lock the pool when the pool page reloads')
def lock_the_pool_when_the_pool_page_reloads(driver):
    """lock the pool when the pool page reloads."""
    assert wait_on_element(driver, 5, '//tr[contains(.,"encrypted_tank")]//mat-icon[text()="more_vert"]', 'clickable')
    driver.find_element_by_xpath('//tr[contains(.,"tank")]//mat-icon[text()="more_vert"]').click()
    assert wait_on_element(driver, 4, '//button[normalize-space(text())="Lock"]', 'clickable')
    driver.find_element_by_xpath('//button[normalize-space(text())="Lock"]').click() 
    assert wait_on_element(driver, 10, '//h1[contains(.,"Lock Dataset encrypted_tank")]')

    assert wait_on_element(driver, 10, '//mat-checkbox[@ix-auto="checkbox__FORCE UNMOUNT"]', 'clickable')
    driver.find_element_by_xpath('//mat-checkbox[@ix-auto="checkbox__FORCE UNMOUNT"]').click()       
    assert wait_on_element(driver, 10, '//mat-checkbox[@ix-auto="checkbox__CONFIRM"]', 'clickable')
    driver.find_element_by_xpath('//mat-checkbox[@ix-auto="checkbox__CONFIRM"]').click()   
    assert wait_on_element(driver, 5, '//button[@ix-auto="button__LOCK"]', 'clickable')
    driver.find_element_by_xpath('//button[@ix-auto="button__LOCK"]').click()

    assert wait_on_element(driver, 10, '//mat-icon[@fonticon="mdi-lock"]')


@then('unlock the pool')
def unlock_the_pool(driver):
    """unlock the pool."""
    assert wait_on_element(driver, 5, '//tr[contains(.,"encrypted_tank")]//mat-icon[text()="more_vert"]', 'clickable')
    driver.find_element_by_xpath('//tr[contains(.,"tank")]//mat-icon[text()="more_vert"]').click()
    assert wait_on_element(driver, 4, '//button[normalize-space(text())="Unlock"]', 'clickable')
    driver.find_element_by_xpath('//button[normalize-space(text())="Unlock"]').click() 
    assert wait_on_element(driver, 10, '//h1[contains(.,"Unlock Datasets")]')
    
    assert wait_on_element(driver, 5, '//input[@ix-auto="input__Dataset Passphrase"]', 'inputable')
    driver.find_element_by_xpath('//input[@ix-auto="input__Dataset Passphrase"]').clear()
    driver.find_element_by_xpath('//input[@ix-auto="input__Dataset Passphrase"]').send_keys("abcd1234")
    assert wait_on_element(driver, 5, '//button[@ix-auto="button__SAVE"]', 'clickable')
    driver.find_element_by_xpath('//button[@ix-auto="button__SAVE"]').click()

    assert wait_on_element(driver, 10, '//p[contains(.,"These datasets will be unlocked with the provided credentials.")]')
    assert wait_on_element(driver, 5, '//button[@ix-auto="button__CONTINUE"]', 'clickable')
    driver.find_element_by_xpath('//button[@ix-auto="button__CONTINUE"]').click()

    assert wait_on_element(driver, 10, '//p[contains(.,"These datasets were successfully unlocked.")]')
    assert wait_on_element(driver, 5, '//button[@ix-auto="button__CONTINUE"]', 'clickable')
    driver.find_element_by_xpath('//button[@ix-auto="button__CONTINUE"]').click()

    assert wait_on_element(driver, 10, '//mat-icon[@fonticon="mdi-lock-open-variant"]')
