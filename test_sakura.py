# coding:utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains
import requests
from pyzbar.pyzbar import decode
from PIL import Image


#新規会員登録
def user_register():
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('新規会員登録').click()
    print(driver.current_url)
    driver.find_element_by_class_name('c-term').find_element_by_tag_name('label').click()  #利用規約同意にチェック
    driver.find_element_by_name('mail_address').send_keys(user_mail_address)  #メールアドレス記載
    driver.find_element_by_class_name('inquiry_form').find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    print("メールアドレス送信")

    # javascriptで新しいページを開く
    driver.execute_script("window.open(arguments[0], 'newtab')", 'https://tix-dev.kadcul.com/admin/')
    time.sleep(3) # ロード分
    allHandles = driver.window_handles

    #新しいタブへ移動
    driver.switch_to_window(allHandles[1])
    # ログイン
    print(driver.current_url)
    if 'login' in driver.current_url:
        driver.find_element_by_id('email').send_keys(admin_mail_address)
        driver.find_element_by_id('password').send_keys(admin_password)
        driver.find_element_by_class_name('btn-info').click()
    driver.get(admin_Auth_codo_url)
    print(driver.current_url)
    #該当ユーザーが何番目かを確認
    for i, lists in enumerate(driver.find_element_by_id('panel1').find_elements_by_tag_name('tr')):
       users = lists.find_elements_by_tag_name('td')
       for g, name in enumerate(users):
        if name.text == user_mail_address:
            user_num = i
    print(user_num)
    first_code = driver.find_element_by_id('panel1').find_elements_by_tag_name('tr')[user_num].find_elements_by_tag_name('td')[2].text
    print(first_code)

    #前のタブへ移動 承認コードを入力
    driver.switch_to_window(allHandles[0])
    driver.find_element_by_id('auth_code').send_keys(first_code)
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)

    #パスワードを登録
    driver.find_element_by_id('password').send_keys(user_password)
    driver.find_element_by_id('password_confirmation').send_keys(user_password)
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    register_text = driver.find_element_by_class_name('txtc').text
    assert register_text == "会員登録が完了しました。", "会員登録失敗"

    print("会員登録完了")


#ログアウト
def user_logout():
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('ログアウト').click()
    print(driver.current_url)
    print("ログアウト")


#ログイン
def user_login():
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('ログイン').click()
    # ログインページ
    print(driver.current_url)
    driver.find_element_by_name('mail_address').send_keys(user_mail_address)
    driver.find_element_by_name('password').send_keys(user_password)
    driver.find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    print("ログイン")


#会員情報登録
def user_profile_register():
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('お客様情報確認').click()
    print(driver.current_url)
    driver.find_elements_by_class_name('p-mypage__table-wrap')[0].find_element_by_class_name('p-mypage__icon').click()
    print(driver.current_url)
    #会員情報記入
    driver.find_element_by_id('last_name').send_keys(user_last_name)
    driver.find_element_by_id('first_name').send_keys(user_first_name)
    driver.find_element_by_id('last_name_kana').send_keys(user_last_name_kana)
    driver.find_element_by_id('first_name_kana').send_keys(user_first_name_kana)
    #生年月日(年)
    year_number_element = driver.find_element_by_name('birthday_year')
    year_nunerr_select_element = Select(year_number_element)
    year_nunerr_select_element.select_by_value(str(birth_year))
    #生年月日(月)
    month_number_element = driver.find_element_by_name('birthday_month')
    month_nunerr_select_element = Select(month_number_element)
    month_nunerr_select_element.select_by_value(str(birth_month))
    #生年月日(日)
    day_number_element = driver.find_element_by_name('birthday_day')
    day_nunerr_select_element = Select(day_number_element)
    day_nunerr_select_element.select_by_value(str(birth_day))
    #性別
    driver.find_element_by_class_name('c-form__radio-list').find_elements_by_tag_name('label')[gender].click()  #性別をクリック
    #郵便番号
    driver.find_element_by_id('postal_code_1').send_keys(postal_code_1)
    driver.find_element_by_id('postal_code_2').send_keys(postal_code_2)

    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click() #確認ボタンを押す

    print(driver.current_url)

    user_name = driver.find_element_by_tag_name('table').find_elements_by_tag_name('td')[0].text
    user_name_kana = driver.find_element_by_tag_name('table').find_elements_by_tag_name('td')[1].text
    user_gender = driver.find_element_by_tag_name('table').find_elements_by_tag_name('td')[2].text
    user_postal_code = driver.find_element_by_tag_name('table').find_elements_by_tag_name('td')[3].text

    print("名前：" + user_name)
    print("名前[カナ]：" + user_name_kana)
    print("生年月日：" + user_gender)
    print("郵便番号：" + user_postal_code)

    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click() #確認ボタンを押す
    print(driver.current_url)
    print("会員登録完了")

    #assert確認
    driver.get(web_url)
    driver.find_element_by_link_text('お客様情報確認').click()
    user_name = driver.find_element_by_class_name('c-table').find_element_by_tag_name('td').text
    print(user_name)
    user_kana = driver.find_element_by_class_name('c-table').find_elements_by_tag_name('td')[1].text
    print(user_kana)
    user_birth = driver.find_element_by_class_name('c-table').find_elements_by_tag_name('td')[2].text
    print(user_birth)
    regist_gender = driver.find_element_by_class_name('c-table').find_elements_by_tag_name('td')[3].text
    print(regist_gender)
    postal = driver.find_element_by_class_name('c-table').find_elements_by_tag_name('td')[4].text
    print(postal)
    assert user_name == user_last_name + user_first_name, "会員登録失敗(名前)"
    assert user_kana == user_last_name_kana + user_first_name_kana, "会員登録失敗(カナ)"
    assert user_birth == str(birth_year)+"年"+str(birth_month)+"月"+str(birth_day)+"日", "会員登録失敗(生年月日)"
    if gender == 0:
        assert regist_gender == "男性", "会員登録失敗(性別)"
    elif gender == 1:
        assert regist_gender == "女性", "会員登録失敗(性別)"
    else:
        assert regist_gender == "その他", "会員登録失敗(性別)"
    assert postal == "〒"+str(postal_code_1)+"-"+str(postal_code_2), "会員登録失敗(郵便番号)"


#会員情報編集
def user_profile_edit():
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('お客様情報確認').click()
    print(driver.current_url)
    driver.find_elements_by_class_name('p-mypage__table-wrap')[0].find_element_by_class_name('p-mypage__icon').click()
    print(driver.current_url)
    #会員情報記入
    driver.find_element_by_id('last_name').clear()
    driver.find_element_by_id('last_name').send_keys(edit_user_last_name)
    driver.find_element_by_id('first_name').clear()
    driver.find_element_by_id('first_name').send_keys(edit_user_first_name)
    driver.find_element_by_id('last_name_kana').clear()
    driver.find_element_by_id('last_name_kana').send_keys(edit_user_last_name_kana)
    driver.find_element_by_id('first_name_kana').clear()
    driver.find_element_by_id('first_name_kana').send_keys(edit_user_first_name_kana)
    #生年月日(年)
    year_number_element = driver.find_element_by_name('birthday_year')
    year_nunerr_select_element = Select(year_number_element)
    year_nunerr_select_element.select_by_value(str(edit_birth_year))
    #生年月日(月)
    month_number_element = driver.find_element_by_name('birthday_month')
    month_nunerr_select_element = Select(month_number_element)
    month_nunerr_select_element.select_by_value(str(edit_birth_month))
    #生年月日(日)
    day_number_element = driver.find_element_by_name('birthday_day')
    day_nunerr_select_element = Select(day_number_element)
    day_nunerr_select_element.select_by_value(str(edit_birth_day))
    #性別
    driver.find_element_by_class_name('c-form__radio-list').find_elements_by_tag_name('label')[edit_gender].click()  #性別をクリック
    #郵便番号
    driver.find_element_by_id('postal_code_1').clear()
    driver.find_element_by_id('postal_code_1').send_keys(edit_postal_code_1)
    driver.find_element_by_id('postal_code_2').clear()
    driver.find_element_by_id('postal_code_2').send_keys(edit_postal_code_2)

    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click() #確認ボタンを押す

    print(driver.current_url)

    user_name = driver.find_element_by_tag_name('table').find_elements_by_tag_name('td')[0].text
    user_name_kana = driver.find_element_by_tag_name('table').find_elements_by_tag_name('td')[1].text
    user_gender = driver.find_element_by_tag_name('table').find_elements_by_tag_name('td')[2].text
    user_postal_code = driver.find_element_by_tag_name('table').find_elements_by_tag_name('td')[3].text

    print("編集名前：" + user_name)
    print("編集名前[カナ]：" + user_name_kana)
    print("編集生年月日：" + user_gender)
    print("編集郵便番号：" + user_postal_code)

    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click() #確認ボタンを押す
    print(driver.current_url)
    print("会員情報編集完了")

#メールアドレス変更
def mail_address_edit():
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('お客様情報確認').click()
    print(driver.current_url)
    driver.find_elements_by_class_name('p-mypage__table-wrap')[1].find_element_by_class_name('p-mypage__icon').click()
    print(driver.current_url)
    driver.find_element_by_name('mail_address').send_keys(edit_user_mail_address)  #メールアドレス記載
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    print("メールアドレス送信")

    allHandles = driver.window_handles

    #新しいタブへ移動
    driver.switch_to_window(allHandles[1])

    # ログイン
    print(driver.current_url)
    if 'login' in driver.current_url:
        driver.find_element_by_id('email').send_keys(admin_mail_address)
        driver.find_element_by_id('password').send_keys(admin_password)
        driver.find_element_by_class_name('btn-info').click()
    driver.get(admin_Auth_codo_url)
    print(driver.current_url)
    #タブの切り替え
    driver.find_element_by_class_name('tab_area').find_elements_by_tag_name('label')[1].click()
    time.sleep(1)
    #該当ユーザーが何番目かを確認
    for i, lists in enumerate(driver.find_element_by_id('panel2').find_elements_by_tag_name('tr')):
       users = lists.find_elements_by_tag_name('td')
       for g, name in enumerate(users):
        if name.text == edit_user_mail_address:
            user_num = i
    print(user_num)
    second_code = driver.find_element_by_id('panel2').find_elements_by_tag_name('tr')[user_num].find_elements_by_tag_name('td')[2].text
    print(second_code)

    #前のタブへ移動 承認コードを入力
    driver.switch_to_window(allHandles[0])
    driver.find_element_by_id('auth_code').send_keys(second_code)
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)

    if driver.find_element_by_class_name('page_title').text == '登録完了':  #クレジット決済の場合
        print("メールアドレスの変更完了")
    else:
        raise Exception('メールアドレスの変更失敗')

    #assert確認
    driver.get(web_url)
    driver.find_element_by_link_text('お客様情報確認').click()
    mail = driver.find_elements_by_class_name('c-table')[1].find_element_by_tag_name('td').text
    print(mail)
    assert mail == edit_user_mail_address, "メールアドレス変更失敗"


#メールアドレス変更をもとに戻す
def mail_address_undo():
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('お客様情報確認').click()
    print(driver.current_url)
    driver.find_elements_by_class_name('p-mypage__table-wrap')[1].find_element_by_class_name('p-mypage__icon').click()
    print(driver.current_url)
    driver.find_element_by_name('mail_address').send_keys(user_mail_address)  #メールアドレス記載
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    print("メールアドレス送信")

    allHandles = driver.window_handles

    #新しいタブへ移動
    driver.switch_to_window(allHandles[1])

    # ログイン
    print(driver.current_url)
    if 'login' in driver.current_url:
        driver.find_element_by_id('email').send_keys(admin_mail_address)
        driver.find_element_by_id('password').send_keys(admin_password)
        driver.find_element_by_class_name('btn-info').click()
    driver.get(admin_Auth_codo_url)
    print(driver.current_url)
    #タブの切り替え
    driver.find_element_by_class_name('tab_area').find_elements_by_tag_name('label')[1].click()
    time.sleep(1)
    #該当ユーザーが何番目かを確認
    for i, lists in enumerate(driver.find_element_by_id('panel2').find_elements_by_tag_name('tr')):
       users = lists.find_elements_by_tag_name('td')
       for g, name in enumerate(users):
        if name.text == user_mail_address:
            user_num = i
    print(user_num)
    third_code = driver.find_element_by_id('panel2').find_elements_by_tag_name('tr')[user_num].find_elements_by_tag_name('td')[2].text
    print(third_code)

    #前のタブへ移動 承認コードを入力
    driver.switch_to_window(allHandles[0])
    driver.find_element_by_id('auth_code').send_keys(third_code)
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)

    if driver.find_element_by_class_name('page_title').text == '登録完了':  #クレジット決済の場合
        print("メールアドレスを元にに戻しました")
    else:
        raise Exception('メールアドレスの変更失敗')


#パスワード再設定(再設定して、元に戻す)
def password_reset():
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('ログアウト').click()
    print(driver.current_url)
    print("ログアウト")
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('ログイン').click()
    # ログインページ
    print(driver.current_url)
    driver.find_element_by_class_name("mat1").click()
    print(driver.current_url)
    driver.find_element_by_name('mail_address').send_keys(user_mail_address)  #メールアドレス記載
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    print("メールアドレス送信")


    allHandles = driver.window_handles

    #新しいタブへ移動
    driver.switch_to_window(allHandles[1])

    # ログイン
    print(driver.current_url)
    if 'login' in driver.current_url:
        driver.find_element_by_id('email').send_keys(admin_mail_address)
        driver.find_element_by_id('password').send_keys(admin_password)
        driver.find_element_by_class_name('btn-info').click()
    driver.get(admin_Auth_codo_url)
    print(driver.current_url)
    #タブの切り替え
    driver.find_element_by_class_name('tab_area').find_elements_by_tag_name('label')[2].click()
    time.sleep(1)

    fourth_code = driver.find_element_by_id('panel3').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].text
    print(fourth_code)

    #前のタブへ移動 承認コードを入力
    driver.switch_to_window(allHandles[0])
    driver.find_element_by_id('auth_code').send_keys(fourth_code)
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)


    #パスワード入力
    driver.find_element_by_id('password').send_keys(edit_user_password)
    driver.find_element_by_id('password_confirmation').send_keys(edit_user_password)
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)

    if driver.find_element_by_class_name('page_title').find_element_by_tag_name("h2").text == 'パスワード再発行完了':
        print("パスワード再発行完了")
    else:
        raise Exception('パスワード再発行失敗')


    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('ログイン').click()
    # ログインページ
    print(driver.current_url)
    driver.find_element_by_name('mail_address').send_keys(user_mail_address)
    driver.find_element_by_name('password').send_keys(edit_user_password)
    driver.find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    print("ログイン")
    #お客様情報⇒パスワード変更
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('お客様情報確認').click()
    print(driver.current_url)
    driver.find_elements_by_class_name('p-mypage__table-wrap')[2].find_element_by_class_name('p-mypage__icon').click()
    print(driver.current_url)
    #変更前パスワード、新パスワード、パスワード確認を入力
    driver.find_element_by_name('old-password').send_keys(edit_user_password)
    driver.find_element_by_name('password').send_keys(user_password)
    driver.find_element_by_name('password_confirmation').send_keys(user_password)
    driver.find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    driver.find_element_by_class_name('btn_main').click()
    print(driver.current_url)


    if driver.find_element_by_class_name('page_title').find_element_by_tag_name("h2").text == 'パスワード変更完了':
        print("パスワード変更完了")
    else:
        raise Exception('パスワード変更失敗')


#クレジットカード追加
def creditcard_add():
    driver.get(web_url)
    print(driver.current_url)
    #お客様情報⇒クレジット追加
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('お客様情報確認').click()
    print(driver.current_url)
    driver.find_elements_by_class_name('p-mypage__table-wrap')[4].find_element_by_class_name('p-mypage__icon').click()
    print(driver.current_url)

    # クレジットカード番号入力
    driver.find_element_by_name('cardNumber').send_keys("4111111111111111")
    #有効期限入力(月を12月にセット)
    number_element = driver.find_element_by_name('cardExpirationMonth')
    nunerr_select_element = Select(number_element)
    nunerr_select_element.select_by_value('12')
    #セキュリティコード入力
    driver.find_element_by_name('security_code').send_keys("123")
    #セキュリティコード入力
    driver.find_element_by_name('holder_name').send_keys("SHOTA NAKAGUCHI")
    time.sleep(1)
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    time.sleep(1)
    print(driver.current_url)
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)

    if driver.find_element_by_class_name('page_title').find_element_by_tag_name("h2").text == 'クレジットカード情報登録完了':
        print("クレジットカード情報登録完了")
    else:
        raise Exception('クレジットカード情報登録失敗')

    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    card = driver.find_elements_by_class_name('p-mypage__credit')[0].find_element_by_tag_name("li").text
    print(card)
    assert str(card) =="**** **** **** *111", "クレジットカード登録失敗"



#クレジットカード削除
def creditcard_delete():
    driver.get(web_url)
    print(driver.current_url)
    #お客様情報⇒クレジット追加
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('お客様情報確認').click()
    print(driver.current_url)
    driver.find_elements_by_class_name('p-mypage__credit')[0].find_element_by_class_name('p-mypage__icon').click()
    print(driver.current_url)
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)


    if driver.find_element_by_class_name('page_title').find_element_by_tag_name("h2").text == 'クレジットカード情報削除完了':
        print("クレジットカード情報削除完了")
    else:
        raise Exception('クレジットカード情報削除失敗')

#チケット購入
def ticket_reserve(turn):
    # TOP
    driver.get(web_url)
    print(driver.current_url)


    if len(driver.find_element_by_id("header_subnav").find_elements_by_tag_name("li")) == 3:
        driver.find_element_by_link_text('ログイン').click()
        # ログインページ
        print(driver.current_url)
        driver.find_element_by_name('mail_address').send_keys(user_mail_address)
        driver.find_element_by_name('password').send_keys(user_password)
        driver.find_element_by_class_name('btn_main').click()

    # チケット選択画面起動
    print(driver.current_url)

    full_day = len(driver.find_elements_by_class_name("day-cell"))  #day-cellを持つものをすべて拾ってくる
    print("full_day"+str(full_day))
    secret_day = len(driver.find_elements_by_class_name("datepicker-item-gray"))  #先月と来月も表示されているのでその分をさせ引く
    print("secret_day"+str(secret_day))
    day_count = full_day - secret_day  #今月が何日あるかを計算する
    print("day_count"+str(day_count))
    print(now_day + after_day + turn )
    if day_count >= now_day + after_day + turn :  #選択する日にちが今月の場合
        print("今月を購入")
        for i, g in enumerate(driver.find_elements_by_class_name('day-cell')): # element"s"にすることでリストで取得できる
            if g.find_element_by_class_name('day-cell--day').text == str(now_day + after_day + turn): #周回ごとに日付を＋1
                g.click()
                break
    else:  #選択する日にちが来月になる場合
        print("来月を購入")
        driver.find_element_by_class_name('glyphicon-chevron-right').click()
        next_month_day = now_day + after_day + turn - day_count  #来月の選択する日にちを計算する
        for i, g in enumerate(driver.find_elements_by_class_name('day-cell')): # element"s"にすることでリストで取得できる
            if g.find_element_by_class_name('day-cell--day').text == str(next_month_day): #周回ごとに日付を＋1
                g.click()
                break

    time.sleep(3) # ロード分

    # チケット1個目を選択
    driver.find_element_by_id('ticketSelect_body').find_element_by_tag_name('table').find_elements_by_tag_name('tr')[turn].find_element_by_tag_name('th').find_element_by_tag_name('h3').click()
    time.sleep(1)
    # 一般を1枚選択
    driver.find_elements_by_class_name('fa-plus')[0].click()

    #購入が2周目の時にクーポンによる購入を行う
    if turn == 1:
        # 一般をもう1枚選択
        driver.find_elements_by_class_name('fa-plus')[0].click()

        #クーポンコードを拾いに行く
        allHandles = driver.window_handles
        #新しいタブへ移動
        driver.switch_to_window(allHandles[1])
        # ログイン
        print(driver.current_url)
        if 'login' in driver.current_url:
            driver.find_element_by_id('email').send_keys(admin_mail_address)
            driver.find_element_by_id('password').send_keys(admin_password)
            driver.find_element_by_class_name('btn-info').click()
        driver.get(admin_invite_list_url)#クーポンコード一覧を開く

        print(driver.current_url)

        #クーポンのグループを選択
        group_number_element = driver.find_element_by_name('invite_code_group_id')
        group_nunerr_select_element = Select(group_number_element)
        group_nunerr_select_element.select_by_value(str(invite_code_group_id))
        print(driver.current_url)
        #未使用クーポンを選択
        unused_number_element = driver.find_element_by_name('search_type')
        unused_nunerr_select_element = Select(unused_number_element)
        unused_nunerr_select_element.select_by_value(search_type_unused)
        print(driver.current_url)

        invite_code = driver.find_element_by_id('table_list_0').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].text
        print(invite_code)

        #前のタブへ移動 承認コードを入力
        driver.switch_to_window(allHandles[0])

        # クーポン利用を選択（p-ticketSelect__footer-itemの1個目）
        driver.find_elements_by_class_name('p-ticketSelect__footer-item')[0].click()
        #クーポンコード入力画面にてクーポンコードを入力
        driver.find_element_by_name('coupon_code').send_keys(invite_code)
        driver.find_element_by_class_name('p-ticketSelect__coupon-footer').find_element_by_tag_name('button').click()  #完了を押す
        print("クーポン入力完了")
        time.sleep(5)

    # 決済へ進むを選択（p-ticketSelect__footer-itemの2個目）
    driver.find_elements_by_class_name('p-ticketSelect__footer-item')[1].click()

    # チケット購入確認画面
    print(driver.current_url)
    # クレジットカード決済を選択
    driver.find_element_by_class_name('p-reserved__credit-head').find_element_by_tag_name('th').find_element_by_tag_name('label').click()
    time.sleep(1) # アニメーション分

    #購入選択日が2日以内かどうか(決済方法でコンビニ決済を選択できるかどうか)
    if now_day + after_day + turn - now_day > 2:
        print("2日以上先の購入")
        print(now_day + after_day + turn)
        if ((now_day + after_day + turn) % 2) == 1 or ((now_day + after_day + turn) % 2) == 0:
            #クレジットカード購入
            print("クレジット購入")
            #クレジットカード登録があるかの条件分岐
            if driver.find_element_by_name('cardNumber').is_displayed():
                print("カードなし")
                # クレジットカード番号入力
                driver.find_element_by_name('cardNumber').send_keys("4111111111111111")
                #有効期限入力(月を12月にセット)
                number_element = driver.find_element_by_name('cardExpirationMonth')
                nunerr_select_element = Select(number_element)
                nunerr_select_element.select_by_value('12')
                #セキュリティコード入力
                driver.find_element_by_name('security_code').send_keys("123")
                #セキュリティコード入力
                driver.find_element_by_name('holder_name').send_keys("SHOTA NAKAGUCHI")
                #driver.find_element_by_name('cardExpirationMonth').send_keys("4111111111111111")
                print("カード入力完了")
            else:
                print("カードあり")
                driver.find_element_by_id('credit-select-block').find_element_by_tag_name('li').find_element_by_tag_name('div').click()
        else:  #奇数日であればコンビニ購入
            print("コンビニ購入")
            driver.find_element_by_class_name('p-reserved__convenience-head').find_element_by_tag_name('th').click()  #コンビニ決済をクリック
            print("コンビニクリック")
            time.sleep(1)
            driver.find_element_by_name('input_cvs_phone_number').send_keys("08012345678")  #適当な電話番号を入力
    else: #二日以内の購入　
        print("2日以内の購入")
        #クレジットカード登録があるかの条件分岐
        if driver.find_element_by_name('cardNumber').is_displayed():
            print("カードなし")
            # クレジットカード番号入力
            driver.find_element_by_name('cardNumber').send_keys("4111111111111111")
            #有効期限入力(月を12月にセット)
            number_element = driver.find_element_by_name('cardExpirationMonth')
            nunerr_select_element = Select(number_element)
            nunerr_select_element.select_by_value('12')
            #セキュリティコード入力
            driver.find_element_by_name('security_code').send_keys("123")
            #セキュリティコード入力
            driver.find_element_by_name('holder_name').send_keys("SHOTA NAKAGUCHI")
            #driver.find_element_by_name('cardExpirationMonth').send_keys("4111111111111111")
            print("カード入力完了")
        else:
            print("カードあり")
            driver.find_element_by_id('credit-select-block').find_element_by_tag_name('li').find_element_by_tag_name('div').click()


    # 利用規約に同意をチェック
    driver.find_element_by_class_name('c-message__text').find_element_by_tag_name('label').click()
    # 確認する
    driver.find_element_by_id('confirmBtn').click()
    time.sleep(1) # アニメーション分
    # 購入する
    driver.find_element_by_id('payment_btn').click()
    time.sleep(1)

    # チケット購入結果画面
    print(driver.current_url)

    if driver.find_element_by_class_name('page_title').text == '購入完了':  #クレジット決済の場合
        bought_ticket_name = driver.find_element_by_class_name('c-table--contents-side').find_element_by_tag_name('table').find_element_by_tag_name('th').text
        bought_ticket_day = driver.find_element_by_class_name('c-table--side').find_element_by_tag_name('td').text
        bought_ticket_price = driver.find_elements_by_class_name('c-table--side')[1].find_elements_by_tag_name('td')[1].text
        print("来場予定が" + bought_ticket_day + "の" + bought_ticket_name + "を購入")  #購入内容を確認
        print("請求金額は" + bought_ticket_price + "です")
        if turn == 1: #クーポン使用の場合値引き額表示
            discount = driver.find_elements_by_class_name('c-table--side')[1].find_elements_by_tag_name('td')[1].text
            print("クーポン利用で" + str(discount) + "です")
            bought_ticket_price = driver.find_elements_by_class_name('c-table--side')[1].find_elements_by_tag_name('td')[2].text
            print(bought_ticket_price)
        else:
            bought_ticket_price = driver.find_elements_by_class_name('c-table--side')[1].find_elements_by_tag_name('td')[1].text
            print(bought_ticket_price)
        # TOPページへ
        driver.find_elements_by_class_name('c-form__item')[1].find_element_by_tag_name('button').click()
        print("チケット購入完了(クレジット)")
    elif driver.find_element_by_class_name('page_title').text == '予約完了（コンビニ決済支払前）':
        # TOPページへ
        driver.find_element_by_class_name('c-form__item').find_element_by_tag_name('button').click()
        print("チケット購入完了(コンビニ)")
    elif driver.find_element_by_class_name('page_title').text == '購入完了':
        raise Exception('チケット購入失敗')
    else:
        raise Exception('チケット購入失敗')

    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_tag_name('nav').find_elements_by_tag_name('li')[5].click()
    print(driver.current_url)
    driver.find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    driver.find_element_by_class_name('p-reservations--history__button').click()
    print(driver.current_url)
    time.sleep(10)

    print("購入詳細")
    details_ticket_name = driver.find_element_by_class_name('c-table--contents-side').find_element_by_tag_name('table').find_element_by_tag_name('p').text
    details_ticket_day = driver.find_element_by_class_name('c-table--side').find_element_by_tag_name('td').text
    print(details_ticket_name)
    print(details_ticket_day)
    details_ticket_price_label = driver.find_elements_by_class_name('c-table--side')[3].find_element_by_tag_name('th').text
    if turn == 1:
        details_ticket_price = driver.find_elements_by_class_name('c-table--side')[3].find_element_by_tag_name('td').text
    else:
        details_ticket_price = driver.find_elements_by_class_name('c-table--side')[2].find_element_by_tag_name('td').text
    print(details_ticket_price_label)
    print(details_ticket_price)

    assert details_ticket_name == bought_ticket_name,"購入情報が間違っています(チケット名)"
    assert details_ticket_day == bought_ticket_day,"購入情報が間違っています(来場日)"
    assert details_ticket_price == bought_ticket_price,"購入情報が間違っています(チケット価格)"

#チケットキャンセル
def ticket_cancel():
    # ログイン
    driver.get(admin_url)
    print(driver.current_url)
    if 'login' in driver.current_url:
        driver.find_element_by_id('email').send_keys(admin_mail_address)
        driver.find_element_by_id('password').send_keys(admin_password)
        driver.find_element_by_class_name('btn-info').click()

    # 会員検索
    print(driver.current_url)

    #element = driver.find_element_by_link_text('会員検索')
    #driver.execute_script('arguments[0].click();', element)
    driver.get("https://tix-dev.kadcul.com/admin/user/top")
    driver.find_element_by_name('mail_address').send_keys(user_mail_address)
    driver.find_element_by_class_name('input-group-text').click()

    # 会員検索
    print(driver.current_url)
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #time.sleep(2)
    element = driver.find_element_by_link_text('詳細を見る')
    driver.execute_script('arguments[0].click();', element)

    # 購入詳細
    print(driver.current_url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.find_element_by_class_name('btn-danger').click()

    # キャンセル確認
    print(driver.current_url)
    time.sleep(2)
    driver.find_element_by_class_name('btn-danger').click()

    # キャンセル結果
    print(driver.current_url)
    if driver.find_element_by_class_name('alert').text != 'キャンセルしました。':
        raise Exception('チケットキャンセル失敗')

    print("チケットキャンセル完了")

#パスポート購入
def passport_reserve():
    print("パスポート購入開始")
    driver.get(web_url)
    print(driver.current_url)

    #パスポート購入(パスポートの購入はこちらをクリック)
    driver.find_element_by_class_name('link').click()
    time.sleep(3) # ロード分

    #パスポート1個目を選択
    driver.find_element_by_id('ticketSelect_body').find_element_by_tag_name('table').find_element_by_tag_name('tr').find_element_by_tag_name('th').find_element_by_tag_name('h3').click()
    # 一般を1枚選択
    time.sleep(3) # ロード分
    driver.find_element_by_class_name('fa-plus').click()
    # 決済へ進むを選択
    driver.find_element_by_class_name('p-ticketSelect__footer-item--passport').click()

    # チケット購入確認画面
    print(driver.current_url)
    # クレジットカード決済を選択
    driver.find_element_by_class_name('p-reserved__credit-head').find_element_by_tag_name('th').find_element_by_tag_name('label').click()
    time.sleep(1) # アニメーション分
    #クレジットカード登録があるかの条件分岐
    if driver.find_element_by_name('cardNumber').is_displayed():
        print("カードなし")
        # クレジットカード番号入力
        driver.find_element_by_name('cardNumber').send_keys("4111111111111111")
        #有効期限入力(月を12月にセット)
        number_element = driver.find_element_by_name('cardExpirationMonth')
        nunerr_select_element = Select(number_element)
        nunerr_select_element.select_by_value('12')
        #セキュリティコード入力
        driver.find_element_by_name('security_code').send_keys("123")
        #セキュリティコード入力
        driver.find_element_by_name('holder_name').send_keys("SHOTA NAKAGUCHI")
        #driver.find_element_by_name('cardExpirationMonth').send_keys("4111111111111111")
        print("カード入力完了")
    else:
        print("カードあり")
        driver.find_element_by_id('credit-select-block').find_element_by_tag_name('li').find_element_by_tag_name('div').click()
    # 購入規約に同意
    driver.find_element_by_class_name('c-message__text').find_element_by_tag_name('label').click()
    # 確認する
    driver.find_element_by_id('confirmBtn').click()
    time.sleep(1) # アニメーション分
    # 購入する
    driver.find_element_by_id('payment_btn').click()
    time.sleep(1)

    # チケット購入結果画面
    print(driver.current_url)

    if driver.find_element_by_class_name('page_title').text != '購入完了':
        raise Exception('パスポート購入失敗')

    bought_passport_name = driver.find_element_by_class_name('c-table--contents-side').find_element_by_tag_name('table').find_element_by_tag_name('th').text
    bought_passport_price = driver.find_element_by_class_name('c-table--side').find_elements_by_tag_name('td')[1].text

    print("購入パスポートは" + bought_passport_name)  #購入内容を確認
    print("請求金額は" + bought_passport_price + "です")


    # TOPページへ
    driver.find_elements_by_class_name('c-form__item')[1].find_element_by_tag_name('button').click()

    print("パスポート購入完了")
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_tag_name('nav').find_elements_by_tag_name('li')[5].click()
    print(driver.current_url)
    driver.find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    driver.find_element_by_class_name('p-reservations--history__button').click()
    print(driver.current_url)
    time.sleep(10)

    details_passport_name = driver.find_element_by_class_name('c-table--contents-side').find_element_by_tag_name('table').find_element_by_tag_name('th').text
    details_passport_price = driver.find_elements_by_class_name('c-table--side')[1].find_element_by_tag_name('td').text

    print(details_passport_name)  #購入内容を確認
    print(details_passport_price )

    assert details_passport_name == bought_passport_name,"購入情報が間違っています(チケット名)"
    assert details_passport_price == bought_passport_price,"購入情報が間違っています(チケット価格)"


#パスポートキャンセル
def passport_cancel(with_ticket):
    # ログイン
    driver.get(admin_url)
    print(driver.current_url)


    if 'login' in driver.current_url:
        driver.find_element_by_id('email').send_keys(admin_mail_address)
        driver.find_element_by_id('password').send_keys(admin_password)
        driver.find_element_by_class_name('btn-info').click()

    # 会員検索
    print(driver.current_url)
    #element = driver.find_element_by_link_text('会員検索')
    #driver.execute_script('arguments[0].click();', element)
    driver.get("https://tix-dev.kadcul.com/admin/user/top")
    driver.find_element_by_name('mail_address').send_keys(user_mail_address)
    driver.find_element_by_class_name('input-group-text').click()

    if with_ticket == 0:
        # 詳細を見るを押す
        print(driver.current_url)

        time.sleep(2)
        element = driver.find_element_by_link_text('詳細を見る')
        driver.execute_script('arguments[0].click();', element)
    else:
        # 詳細を見るを押す
        print(driver.current_url)
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        element = driver.find_elements_by_class_name('table-bordered')[1].find_elements_by_tag_name('tr')[2].find_element_by_link_text('詳細を見る')
        driver.execute_script('arguments[0].click();', element)


    # 購入詳細
    print(driver.current_url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    element = driver.find_element_by_link_text('購入と決済をキャンセル')
    driver.execute_script('arguments[0].click();', element)

    # キャンセル確認
    print(driver.current_url)
    driver.find_element_by_class_name('btn-danger').click()

    # キャンセル結果
    print(driver.current_url)
    if driver.find_element_by_class_name('alert').text != 'キャンセルしました。':
        raise Exception('パスポートキャンセル失敗')

    print("パスポートキャンセル完了")

#パスポート利用によるチケット購入
def ticket_passport_use():

    driver.get(web_url)
    print(driver.current_url)

    if len(driver.find_element_by_id("header_subnav").find_elements_by_tag_name("li")) == 3:
        driver.find_element_by_link_text('ログイン').click()
        # ログインページ
        print(driver.current_url)
        driver.find_element_by_name('mail_address').send_keys(user_mail_address)
        driver.find_element_by_name('password').send_keys(user_password)
        driver.find_element_by_class_name('btn_main').click()

    # 何番目のパスポートかを取得する
    print(driver.current_url)
    for i, passport in enumerate(driver.find_elements_by_class_name('table_box')[1].find_element_by_tag_name('table').find_elements_by_tag_name('p')):
        if passport.text == buy_passport:
            passport_num = i

            print(i)

    #パスポート購入(パスポートの購入はこちらをクリック)
    driver.find_element_by_class_name('link').click()
    time.sleep(3) # ロード分

     #パスポート1個目を選択
    driver.find_element_by_id('ticketSelect_body').find_element_by_tag_name('table').find_elements_by_tag_name('tr')[passport_num].find_element_by_tag_name('th').find_element_by_tag_name('h3').click()
    # 一般を1枚選択
    driver.find_element_by_class_name('fa-plus').click()
    # 決済へ進むを選択
    driver.find_element_by_class_name('p-ticketSelect__footer-item--passport').click()

    # チケット購入確認画面
    print(driver.current_url)
    # クレジットカード決済を選択
    driver.find_element_by_class_name('p-reserved__credit-head').find_element_by_tag_name('th').find_element_by_tag_name('label').click()
    time.sleep(1) # アニメーション分
    #クレジットカード登録があるかの条件分岐
    if driver.find_element_by_name('cardNumber').is_displayed():
        print("カードなし")
        # クレジットカード番号入力
        driver.find_element_by_name('cardNumber').send_keys("4111111111111111")
        #有効期限入力(月を12月にセット)
        number_element = driver.find_element_by_name('cardExpirationMonth')
        nunerr_select_element = Select(number_element)
        nunerr_select_element.select_by_value('12')
        #セキュリティコード入力
        driver.find_element_by_name('security_code').send_keys("123")
        #セキュリティコード入力
        driver.find_element_by_name('holder_name').send_keys("SHOTA NAKAGUCHI")
        #driver.find_element_by_name('cardExpirationMonth').send_keys("4111111111111111")
        print("カード入力完了")
    else:
        print("カードあり")
        driver.find_element_by_id('credit-select-block').find_element_by_tag_name('li').find_element_by_tag_name('div').click()
    # 購入規約に同意
    driver.find_element_by_class_name('c-message__text').find_element_by_tag_name('label').click()
    # 確認する
    driver.find_element_by_id('confirmBtn').click()
    time.sleep(1) # アニメーション分
    # 購入する
    driver.find_element_by_id('payment_btn').click()
    time.sleep(1)

    # チケット購入結果画面
    print(driver.current_url)

    if driver.find_element_by_class_name('page_title').text != '購入完了':
        raise Exception('パスポート購入失敗')

    # TOPページへ
    driver.find_elements_by_class_name('c-form__item')[1].find_element_by_tag_name('button').click()

    print("パスポート購入完了")
    print(driver.current_url)

    full_day = len(driver.find_elements_by_class_name("day-cell"))  #day-cellを持つものをすべて拾ってくる
    secret_day = len(driver.find_elements_by_class_name("datepicker-item-gray"))  #先月と来月も表示されているのでその分をさせ引く
    day_count = full_day - secret_day  #今月が何日あるかを計算する
    if day_count >= now_day + 1:  #選択する日にちが今月の場合
        for i, g in enumerate(driver.find_elements_by_class_name('day-cell')): # element"s"にすることでリストで取得できる
            if g.find_element_by_class_name('day-cell--day').text == str(now_day + 1): #周回ごとに日付を＋1
                g.click()
                break
    else:  #選択する日にちが来月になる場合
        driver.find_element_by_class_name('glyphicon-chevron-right').click()
        next_month_day = now_day + 1 - day_count  #来月の選択する日にちを計算する
        for i, g in enumerate(driver.find_elements_by_class_name('day-cell')): # element"s"にすることでリストで取得できる
            if g.find_element_by_class_name('day-cell--day').text == str(next_month_day): #周回ごとに日付を＋1
                g.click()
                break

    time.sleep(3) # ロード分

    #パスポート所持しているチケットを取得
    for g, ticket in enumerate(driver.find_element_by_class_name('p-ticketSelect__body').find_element_by_tag_name('table').find_elements_by_tag_name('tr')):
        print(ticket.find_element_by_tag_name('span').text)
        print(g)
        if ticket.find_element_by_tag_name('span').text == "パスポート所持中":
            ticket_num = g


    # チケット1個目を選択
    driver.find_element_by_id('ticketSelect_body').find_element_by_tag_name('table').find_elements_by_tag_name('tr')[ticket_num].find_element_by_tag_name('th').find_element_by_tag_name('h3').click()
    time.sleep(1)
    # 一般を2枚選択
    driver.find_elements_by_class_name('fa-plus')[0].click()
    driver.find_elements_by_class_name('fa-plus')[0].click()


    # 決済へ進むを選択（p-ticketSelect__footer-itemの2個目）
    driver.find_elements_by_class_name('p-ticketSelect__footer-item')[1].click()

    # チケット購入確認画面
    print(driver.current_url)
    # クレジットカード決済を選択
    driver.find_element_by_class_name('p-reserved__credit-head').find_element_by_tag_name('th').find_element_by_tag_name('label').click()
    time.sleep(1) # アニメーション分

    if driver.find_element_by_name('cardNumber').is_displayed():
        print("カードなし")
        # クレジットカード番号入力
        driver.find_element_by_name('cardNumber').send_keys("4111111111111111")
        #有効期限入力(月を12月にセット)
        number_element = driver.find_element_by_name('cardExpirationMonth')
        nunerr_select_element = Select(number_element)
        nunerr_select_element.select_by_value('12')
        #セキュリティコード入力
        driver.find_element_by_name('security_code').send_keys("123")
        #セキュリティコード入力
        driver.find_element_by_name('holder_name').send_keys("SHOTA NAKAGUCHI")
        #driver.find_element_by_name('cardExpirationMonth').send_keys("4111111111111111")
        print("カード入力完了")
    else:
        print("カードあり")
        driver.find_element_by_id('credit-select-block').find_element_by_tag_name('li').find_element_by_tag_name('div').click()


      # 利用規約に同意をチェック
    driver.find_element_by_class_name('c-message__text').find_element_by_tag_name('label').click()
    # 確認する
    driver.find_element_by_id('confirmBtn').click()
    time.sleep(1) # アニメーション分
    # 購入する
    driver.find_element_by_id('payment_btn').click()
    time.sleep(1)

    # チケット購入結果画面
    print(driver.current_url)

    if driver.find_element_by_class_name('page_title').text == '購入完了':  #クレジット決済の場合
        bought_ticket_name = driver.find_element_by_class_name('c-table--contents-side').find_element_by_tag_name('table').find_element_by_tag_name('th').text
        bought_ticket_day = driver.find_element_by_class_name('c-table--side').find_element_by_tag_name('td').text
        print("来場予定が" + bought_ticket_day + "の" + bought_ticket_name + "を購入")  #購入内容を確認
        discount = driver.find_elements_by_class_name('c-table--side')[1].find_elements_by_tag_name('td')[1].text
        print("パスポート利用で" + str(discount) + "です")
        bought_ticket_price = driver.find_elements_by_class_name('c-table--side')[1].find_elements_by_tag_name('td')[2].text
        print("請求金額は" + bought_ticket_price + "です")
        # TOPページへ
        driver.find_elements_by_class_name('c-form__item')[1].find_element_by_tag_name('button').click()
        print("チケット購入完了(クレジット)")
    elif driver.find_element_by_class_name('page_title').text == '予約完了（コンビニ決済支払前）':
        # TOPページへ
        driver.find_element_by_class_name('c-form__item').find_element_by_tag_name('button').click()
        print("チケット購入完了(コンビニ)")
    elif driver.find_element_by_class_name('page_title').text == '購入完了':
        raise Exception('チケット購入失敗')
    else:
        raise Exception('チケット購入失敗')

    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_tag_name('nav').find_elements_by_tag_name('li')[5].click()
    print(driver.current_url)
    driver.find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    driver.find_element_by_class_name('p-reservations--history__button').click()
    print(driver.current_url)

    print("購入詳細")

    details_ticket_name = driver.find_element_by_class_name('c-table--contents-side').find_element_by_tag_name('table').find_element_by_tag_name('p').text
    details_ticket_price = driver.find_elements_by_class_name('c-table--side')[3].find_element_by_tag_name('td').text
    details_discount = driver.find_elements_by_class_name('c-table--side')[2].find_element_by_tag_name('td').text

    print(details_ticket_name)  #購入内容を確認
    print(details_ticket_price )
    print(details_discount)

    assert details_ticket_name == bought_ticket_name,"購入情報が間違っています(チケット名)"
    assert details_ticket_price == bought_ticket_price,"購入情報が間違っています(チケット価格)"
    assert details_discount == discount,"購入情報が間違っています(パスポート値引き額が間違っています)"



def staff_in():
    #販売サイトから持ってるチケットの入場可能エリアを取得する
    driver.get(web_url)
    print(driver.current_url)

    time.sleep(1)

    print(day.year)
    print(day.month)
    print(day.day)

    today = str(day.year) + "年" + str(day.month) + "月" + str(day.day) + "日"


    #ページの要素数よりQRが表示されているかいないかを判定する
    qr_check = driver.find_element_by_class_name('inner').find_elements_by_tag_name('article')
    print(len(qr_check))

    if len(qr_check) >= 7:
        print("QR表示されている")

        #訪問日が今日か
        vusit_day = driver.find_element_by_class_name('c-qr__date').find_element_by_tag_name("p").text
        print(today)
        print(vusit_day)
        if today == vusit_day[:-3]:
            print("来場日は今日")
        else:
            print("来場日は今日じゃない")
            return

        driver.find_element_by_class_name('c-qr').find_element_by_class_name('marker').click()
        area = driver.find_element_by_class_name('c-qr').find_element_by_class_name('show-modal').find_elements_by_tag_name('li')[1].text
        print(area[1:])
        #QRを読み込む
        png = driver.find_element_by_tag_name('svg').screenshot_as_png  #QRをスクショ
        with open('./img.png', 'wb') as f:  #スクショ画像を保存
            f.write(png)
        time.sleep(5)
        image = './img.png'  #保存した画像を指定
        data = decode(Image.open(image)) #指定した画像を読む
        code = data[0][0].decode('utf-8', 'ignore')
        print(code)

    else: #QRが表示されていなければ終了
        print("QR表示されていない")
        return

    driver.get(staff_url)
    print(driver.current_url)


    if 'login' in driver.current_url:
        driver.find_element_by_id('email').send_keys(staff_mail_address)
        driver.find_element_by_id('password').send_keys(staff_password)
        driver.find_element_by_class_name('btn-info').click()

    #所持チケットのエリアに入る
    for i, areas in enumerate(driver.find_element_by_class_name('pb-1').find_elements_by_class_name('col-12')):
        #エリアナンバーを取得する
        if areas.find_element_by_tag_name('b').text == area[1:]:
            area_num = i
            print(i)

    time.sleep(1)
    driver.find_element_by_class_name('pb-1').find_elements_by_class_name('col-12')[area_num].click()
    print(driver.current_url)
    befor_url = driver.current_url

    t = driver.find_element_by_name('_token')
    token = t.get_attribute("value")



    # token取得用URL
    #token_url = TOKEN_URL

    # formの送信先のURLを設定
    url = "https://tix-dev.kadcul.com/staff/area/1/inout/check"

    reservation_code = {'_token': str(token) , 'reservation_code': str(code)}
    print(token)
    print(type(token))
    print(code)

    session = requests.session()

     #セッションの受け渡し
    for cookie in driver.get_cookies():
        session.cookies.set(cookie["name"], cookie["value"])
        #headers = {cookie["name"]:  cookie["value"]}

    response = session.get('https://tix-dev.kadcul.com/staff/area/1/reservation/detail')

    response_cookie = response.cookies
    print(response_cookie)
    #<RequestsCookieJar[<Cookie _hogehoge_session=長いので省略
    result = session.post(url, reservation_code, response_cookie)

    driver.get(result.url)

    driver.find_element_by_class_name('btn-success').click()
    print("利用を押した")
    print(driver.current_url)
    after_url = driver.current_url

    driver.get(web_url)
    print(driver.current_url)

    driver.find_element_by_link_text('オンラインチケット確認').click()
    print(driver.current_url)

    driver.find_element_by_class_name('p-reservations__ticket-table').find_elements_by_tag_name('tr')[0].click()
    time.sleep(1)
    use_status = driver.find_element_by_class_name('p-reservations__ticket-table').find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('span')[5].text
    print(use_status)
    assert use_status == "使用済み","チケットの利用が出来ていません"

 #ユーザー退会
def user_withdrawal():
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('お客様情報確認').click()
    print(driver.current_url)
    element = driver.find_element_by_link_text('>退会')
    driver.execute_script('arguments[0].click();', element)
    driver.find_element_by_class_name('checkbox').find_element_by_tag_name('label').click()  #利用規約同意にチェック
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)
     #パスワードを入力
    driver.find_element_by_id('password').send_keys(user_password)
    driver.find_element_by_class_name('btn_area').find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    print("退会完了")


 #kadokawaログイン(※kadokawa idはいったん手動で作成を行っておいた)
def kadokawa_user_register():
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('新規会員登録').click()
    print(driver.current_url)
    driver.find_element_by_class_name('c-term').find_element_by_tag_name('label').click()  #利用規約同意にチェック
    driver.find_elements_by_class_name('inquiry_form')[1].find_element_by_class_name('btn_main').click()
    print(driver.current_url)
    time.sleep(3)  #表示が遅いため調整

    #角川IDサインイン
    driver.find_element_by_id('signInName').send_keys(user_mail_address)  #メールアドレス記載
    driver.find_element_by_id('password').send_keys(user_password)  #パスワード記載
    driver.find_element_by_id('next').click()

    time.sleep(10)


    #連携解除してると紐づけが入る
    if 'kadokawa/register' in driver.current_url:
        driver.find_element_by_id('email').send_keys(user_mail_address)
        driver.find_element_by_id('password').send_keys(user_password)
        driver.find_element_by_id('password_confirmation').send_keys(user_password)
        driver.find_element_by_class_name('btn_main').click()
        print("紐づけ完了")

    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('ログアウト').click()
    print(driver.current_url)
    print("ログアウト")


    #角川IDログイン
    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('ログイン').click()
    # ログインページ
    print(driver.current_url)
    driver.find_elements_by_class_name('btn_main')[1].click()
    print(driver.current_url)
    print("ログイン")

    time.sleep(3)

    driver.get(web_url)
    print(driver.current_url)
    driver.find_element_by_link_text('お客様情報確認').click()
    print(driver.current_url)
    driver.find_elements_by_class_name('p-mypage__table-wrap')[3].find_element_by_class_name('p-mypage__icon').click()
    print("連携解除")


#チケット名変更
def ticket_rename():
     # ログイン
    driver.get(admin_url)
    print(driver.current_url)


    if 'login' in driver.current_url:
        driver.find_element_by_id('email').send_keys(admin_mail_address)
        driver.find_element_by_id('password').send_keys(admin_password)
        driver.find_element_by_class_name('btn-info').click()

    # チケット設定
    print(driver.current_url)
    driver.find_element_by_link_text('チケット設定').click()
    element = driver.find_element_by_link_text('チケット一覧表示')
    driver.execute_script('arguments[0].click();', element)

    #指定したチケットNoの編集ボタンを押す
    for g, rename_ticket in enumerate(driver.find_element_by_class_name('table-bordered').find_elements_by_tag_name('tr')):
        if g == 0:
            continue
        if rename_ticket.find_element_by_tag_name('td').text == str(rename_ticket_no):
            rename_no = g

    print(rename_no)


    # チケット1個目を選択
    driver.find_element_by_class_name('table-bordered').find_elements_by_tag_name('tr')[rename_no].find_element_by_link_text('編集').click()

    print(driver.current_url)

    driver.find_element_by_id('name').clear()
    driver.find_element_by_id('name').send_keys(edit_ticket_name)
    driver.find_element_by_class_name('btn-info').click()
    driver.find_element_by_class_name('btn-success').click()
    print(driver.current_url)
    print("編集完了")

#チケット名変更(＋元のチケット名に戻す)
def ticket_rename_check():
    driver.get(web_url)
    print(driver.current_url)

    # ログインページ
    if len(driver.find_element_by_id("header_subnav").find_elements_by_tag_name("li")) == 3:
        driver.find_element_by_link_text('ログイン').click()
        # ログインページ
        print(driver.current_url)
        driver.find_element_by_name('mail_address').send_keys(user_mail_address)
        driver.find_element_by_name('password').send_keys(user_password)
        driver.find_element_by_class_name('btn_main').click()


    qr_check = driver.find_element_by_class_name('inner').find_elements_by_tag_name('article')
    print(len(qr_check))

    if len(qr_check) >= 7:
        print("QR表示されている")

        changed_ticket_name = driver.find_element_by_class_name('c-qr__ticket-name').find_element_by_tag_name("p").text
        word_count = len(edit_ticket_name)
        bought_ticket_name = changed_ticket_name[:word_count]
        print(bought_ticket_name)
        assert bought_ticket_name == edit_ticket_name,"チケット名が間違っています"
    else: #QRが表示されていなければ終了
        print("QR表示されていない")
        return



    driver.get(admin_url)
    print(driver.current_url)

    # チケット設定
    if 'login' in driver.current_url:
        driver.find_element_by_id('email').send_keys(admin_mail_address)
        driver.find_element_by_id('password').send_keys(admin_password)
        driver.find_element_by_class_name('btn-info').click()

    driver.find_element_by_link_text('チケット設定').click()
    element = driver.find_element_by_link_text('チケット一覧表示')
    driver.execute_script('arguments[0].click();', element)

    #指定したチケットNoの編集ボタンを押す
    for g, rename_ticket in enumerate(driver.find_element_by_class_name('table-bordered').find_elements_by_tag_name('tr')):
        if g == 0:
            continue
        if rename_ticket.find_element_by_tag_name('td').text == str(rename_ticket_no):
            rename_no = g

    print(rename_no)


    # チケット1個目を選択
    driver.find_element_by_class_name('table-bordered').find_elements_by_tag_name('tr')[rename_no].find_element_by_link_text('編集').click()

    print(driver.current_url)

    driver.find_element_by_id('name').clear()
    driver.find_element_by_id('name').send_keys(ticket_name)
    driver.find_element_by_class_name('btn-info').click()
    driver.find_element_by_class_name('btn-success').click()





if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.set_window_size(1280, 1024)
    now_day = datetime.date.today().day
    day = datetime.datetime.now()
    web_url = 'https://tix-dev.kadcul.com/'
    admin_url = 'https://tix-dev.kadcul.com/admin/'
    admin_Auth_codo_url = 'https://tix-dev.kadcul.com/admin/secret/user/auth_code'
    admin_invite_list_url = 'https://tix-dev.kadcul.com/admin/invite/list'
    staff_url = 'https://tix-dev.kadcul.com/staff'
    after_day = 0
    user_mail_address = "nakateconew@gmail.com"
    user_password = "sakura0301"
    admin_mail_address = "sakura.tecotec@gmail.com"
    admin_password = "sakura0301"
    staff_mail_address = "sakura.tecotec@gmail.com"
    staff_password = "sakura0301"
    user_last_name = "中口"
    user_first_name = "翔太"
    user_last_name_kana = "ナカグチ"
    user_first_name_kana = "ショウタ"
    birth_year = 1990
    birth_month = 2
    birth_day = 27
    postal_code_1  = 111
    postal_code_2 = 2222
    gender = 0  #男:0 女:１ その他:2
    #会員情報編集
    edit_user_last_name = "大口"
    edit_user_first_name = "翔子"
    edit_user_last_name_kana = "オオグチ"
    edit_user_first_name_kana = "ショウコ"
    edit_birth_year = 1999
    edit_birth_month = 12
    edit_birth_day = 2
    edit_postal_code_1  = 333
    edit_postal_code_2 = 4444
    edit_gender = 1  #男:0 女:１ その他:2
    edit_user_mail_address = "nakatecoedit@gmail.com"
    edit_user_password = "sakura0401"
    invite_code_group_id = 9 #あらかじめクーポンを用意しておく必要あり、用意しておいたクーポンのグループIDをセット
    search_type_unused = "unused" #未使用のクーポンにフィルタリングする
    buy_passport = "夏休みマンガラノベパス"  #購入パスポートを指定
    rename_ticket_no = 1   #チケット名を変更するチケットIDを指定する
    edit_ticket_name = "自動テスト編集隈展チケット"
    ticket_name = "隈展チケット"



    '''

    # チケット購入
    ticket_reserve(0)

    # チケットキャンセル
    ticket_cancel()

    # パスポート購入
    passport_reserve()

    # パスポートキャンセル
    passport_cancel()

    print("1回目終了")

    time.sleep(10)


    '''

    #新規ユーザー登録
    user_register()

    #ログアウト
    user_logout()

    #ログイン
    user_login()

    #ユーザー情報登録
    user_profile_register()


    #ユーザー情報編集
    user_profile_edit()

    #メールアドレス変更
    mail_address_edit()
    #変更をもとに戻しておく
    mail_address_undo()

    #パスワード再設定(パスワード変更にて元のパスワードに戻すことも含めて)
    password_reset()



    #クレジットカード追加
    creditcard_add()

    #クレジットカード削除
    #creditcard_delete()

    #チケット購入(＋キャンセル)とパスポート購入(＋キャンセル)をn回繰り返す　rangeの設定値で調整
    for i in range(2):
        ticket_reserve(i)
        ticket_cancel()
        passport_reserve()
        passport_cancel(0)
        print(str(i + 1) + "週目終了" )
        time.sleep(5)



    #パスポート利用のチケット購入
    ticket_passport_use()
    ticket_cancel()
    passport_cancel(1)
    print("パスポートによるチケット購入完了")

    #入場
    #user_profile_register()
    ticket_reserve(0)

    staff_in()
    ticket_cancel()


    #ユーザー退会
    user_withdrawal()

    #角川ID関連
    kadokawa_user_register()
    user_withdrawal()

    #チケット名変更(会員登録⇒チケット購入⇒チケット名編集⇒もとに戻す⇒キャンセル⇒退会)
    user_register()
    user_profile_register()
    ticket_rename()
    ticket_reserve(0)
    ticket_rename_check()
    ticket_cancel()
    user_withdrawal()



    time.sleep(5)
    #driver.quit()