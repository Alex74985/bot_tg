import os
import time
import models
import random
import threading
import keyboard
from tool import language_check, create_inlineKeyboard
from app import middleware_base, bot, post_base, end_base
from datetime import datetime
from datetime import timedelta
from models import session
from sqlalchemy import and_


def check_user(user_id):
    user = middleware_base.get_one(models.User, user_id=str(user_id))
    if user != None:
        return user
    else:
        return False


def create_draw_progress(user_id, tmp):
    middleware_base.delete(models.DrawProgress, user_id=(str(user_id)))
    middleware_base.new(models.DrawProgress, str(user_id), tmp['chanel_id'], tmp['draw_text'], tmp['file_type'], tmp['file_id'],
                        int(tmp['winers_count']), tmp['start_time'],
                        tmp['end_time'])  # , tmp['chanel_name'],
    middleware_base.delete(models.State, user_id=str(user_id))

    return draw_info(user_id)


def draw_info(user_id):
    tmp = check_post(str(user_id))
    text = language_check(user_id)[1]['draw']
    return f"{text['change_text']}\n{text['post_time_text']} {tmp.post_time}\n{text['over_time_text']} {tmp.end_time}\n{text['count_text']} {tmp.winers_count}\n{text['text']} {tmp.text}"  # \n{text['chanel/chat']} {tmp.chanel_name}


def check_post(user_id):
    return middleware_base.get_one(models.DrawProgress, user_id=str(user_id))


def send_draw_info(user_id):
    tmp = check_post(str(user_id))
    text = language_check(user_id)[1]['draw']
    draw_text = f"{text['change_text']}\n{text['post_time_text']} {tmp.post_time}\n{text['over_time_text']} {tmp.end_time}\n{text['count_text']} {tmp.winers_count}\n{text['text']} {tmp.text}"  # \n{text['chanel/chat']} {tmp.chanel_name}
    if tmp.file_type == 'photo':
        # if len(draw_text) < 4000:
        #     bot.send_photo(user_id, tmp.file_id, draw_text, reply_markup=keyboard.get_draw_keyboard(user_id))
        # else:
        bot.send_photo(user_id, tmp.file_id)
        bot.send_message(user_id, draw_text, reply_markup=keyboard.get_draw_keyboard(user_id))
    if tmp.file_type == 'document':
        bot.send_document(user_id, tmp.file_id, caption=draw_text, reply_markup=keyboard.get_draw_keyboard(user_id))
    else:
        bot.send_message(user_id, draw_text, reply_markup=keyboard.get_draw_keyboard(user_id))
    middleware_base.delete(models.State, user_id=user_id)


def my_draw_info(user_id, row=0):
    if row < 0:
        return 'first'

    text = language_check(user_id)[1]['my_draw']
    notposted = middleware_base.select_all(models.DrawNot, user_id=str(user_id))
    posted = middleware_base.select_all(models.Draw, user_id=str(user_id))
    all_draws = notposted + posted
    if len(all_draws) == 0:
        bot.send_message(user_id, text['no_draw'])

    if row >= len(all_draws):
        print('notttt')

    try:
        draw_text = f"{text['your_draw']}\n{text['post_time_text']} {all_draws[row].post_time}\n{text['over_time_text']} {all_draws[row].end_time}\n{text['chanel/chat']} {all_draws[row].chanel_name}\n{text['count_text']} {all_draws[row].winers_count}\n{text['text']} {all_draws[row].text}"
        keyboard = create_inlineKeyboard({text['back']: "back", text['next']: "next"}, 2)
        if all_draws[row].file_type == 'photo':
            # if len(draw_text) < 4000:
            #     bot.send_photo(user_id, all_draws[row].file_id, draw_text, reply_markup=keyboard)
            # else:
            bot.send_photo(user_id, all_draws[row].file_id)
            bot.send_message(user_id, draw_text, reply_markup=keyboard)
        elif all_draws[row].file_type == 'document':
            bot.send_document(user_id, all_draws[row].file_id, caption=draw_text, reply_markup=keyboard)
        else:
            bot.send_message(user_id, draw_text, reply_markup=keyboard)
    except Exception as e:
        print(e)
        print(text)
        print(all_draws)


def start_draw_timer():
    def timer():
        while 1:
            for i in post_base.select_all(models.DrawNot):
                if not i.chanel_id:
                    post_base.delete(models.DrawNot, id=str(i.id))
                    continue
                count = 0
                post_time = datetime.now()
                if post_time >= datetime.strptime(i.post_time, '%Y-%m-%d %H:%M'):
                    safed = False
                    if i.file_type == 'photo':
                        # if len(i.text) < 4000:
                        #     tmz = bot.send_photo(
                        #         chanel_id,
                        #         i.file_id,
                        #         i.text,
                        #         parse_mode='HTML', reply_markup=create_inlineKeyboard({language_check(i.user_id)[1]['draw']['get_on']:f'geton_{i.id}'}),
                        #     )
                        # else:
                        tmz = bot.send_photo(
                            i.chanel_id,
                            i.file_id,
                            caption=i.text,
                            parse_mode='HTML', reply_markup=create_inlineKeyboard(
                                {language_check(i.user_id)[1]['draw']['get_on']: f'geton_{i.id}'}),
                        )
                        # tmz = bot.send_message(
                        #     i.chanel_id,
                        #     i.text,
                        #     parse_mode='HTML', reply_markup=create_inlineKeyboard(
                        #         {language_check(i.user_id)[1]['draw']['get_on']: f'geton_{i.id}'}),
                        # )
                    elif i.file_type == 'document':
                        tmz = bot.send_document(
                            i.chanel_id,
                            i.file_id,
                            caption=i.text,
                            parse_mode='HTML',
                            reply_markup=create_inlineKeyboard(
                                {language_check(i.user_id)[1]['draw']['get_on']: f'geton_{i.id}'}),
                        )
                    else:
                        tmz = bot.send_message(
                            i.chanel_id,
                            i.text,
                            parse_mode='HTML',
                            reply_markup=create_inlineKeyboard(
                                {language_check(i.user_id)[1]['draw']['get_on']: f'geton_{i.id}'}),
                        )

                    if safed:
                        continue

                    post_base.new(models.Draw, i.id, i.user_id, tmz.message_id, i.chanel_id, '-', i.text, i.file_type,
                                  i.file_id, i.winers_count, '', i.post_time, i.end_time, i.channels)
                    post_base.delete(models.DrawNot, id=str(i.id))
                    safed = True

            time.sleep(5)

    rT = threading.Thread(target=timer)
    rT.start()


def end_draw_timer():
    def end_timer():
        while 1:
            for i in end_base.select_all(models.Draw):
                count = 0
                post_time = datetime.now()
                session.refresh(i)
                session.commit()
                if post_time >= datetime.strptime(i.end_time, '%Y-%m-%d %H:%M'):
                    text = language_check(i.user_id)[1]['draw']
                    players = end_base.select_all(models.DrawPlayer, draw_id=str(i.id))
                    if players == []:
                        winers = f"\n\n{text['no_winers']}"
                        owin = f"{text['no_winers']}"
                    else:
                        winers = f"\n\n{text['winers']}\n"
                        owin = f"{text['winers']}\n"
                        predicted_winners = []
                        filtered_winners = []
                        for player in players:
                            if player.user_id in str(i.predicted_winners).split():
                                predicted_winners.append(player)
                            else:
                                filtered_winners.append(player)
                        players = filtered_winners
                        pls = {p.user_id: p for p in players}
                        p_w = {p.user_id: p for p in predicted_winners}
                        print('players: ', players)
                        print('pls', pls, len(pls))
                        print('draw: ', i)
                        print('id predicted winner: ', i.predicted_winners)
                        print('predicted_winners', predicted_winners)
                        print('p_w', p_w, len(p_w))
                        for _ in range(min(len(p_w), int(i.winers_count))):
                            predicted_player = random.choice(list(p_w.values()))
                            del p_w[predicted_player.user_id]
                            winers += f"<a href='tg://user?id={predicted_player.user_id}'>{predicted_player.user_name}</a>\n"
                            owin += f"<a href='tg://user?id={predicted_player.user_id}'>{predicted_player.user_name}</a>\n"
                            count += 1
                        for _ in range(min(int(i.winers_count)-len(predicted_winners), len(pls))):
                            random_player = random.choice(list(pls.values()))
                            del pls[random_player.user_id]

                            winers += f"<a href='tg://user?id={random_player.user_id}'>{random_player.user_name}</a>\n"
                            owin += f"<a href='tg://user?id={random_player.user_id}'>{random_player.user_name}</a>\n"
                            count += 1

                    try:
                        bot.send_message(
                            chat_id=str(i.chanel_id),
                            text=winers,
                            parse_mode='HTML',
                        )
                    except:
                        end_base.delete(models.Draw, id=i.id)
                        bot.send_message(i.chanel_id, text['failed_post'])
                        return 'gg'
                    bot.send_message(i.user_id, f"{text['your_draw_over']}\n{owin}", parse_mode='HTML')
                    end_base.delete(models.Draw, id=i.id)
                    time.sleep(1)

            time.sleep(5)

    rT = threading.Thread(target=end_timer)
    rT.start()


def new_player(call):
    id = int(call.data.split('_')[1])
    print('id: ', int(id))
    tmp = middleware_base.get_one(models.Draw, id=id)
    print('tmp: ', tmp)

    if tmp is None:
        return None

    chanel = middleware_base.select_all(models.SubscribeChannel, draw_id=str(tmp.id))
    print('chanel: ', chanel)
    status = ['left', 'kicked', 'restricted']
    for i in chanel:
        if bot.get_chat_member(chat_id=i.channel_id, user_id=call.from_user.id).status in status:
            return 'not_subscribe'

    players = middleware_base.get_one(models.DrawPlayer, draw_id=str(tmp.id), user_id=str(call.from_user.id))
    print('players: ', players)
    if players == None:
        middleware_base.new(models.DrawPlayer, tmp.id, str(call.from_user.id),
                            str(call.from_user.username) if call.from_user.username else f"id{call.from_user.id}")
        tmz = middleware_base.select_all(models.DrawPlayer, draw_id=str(tmp.id))
        return (len(tmz), language_check(tmp.user_id)[1]['draw']['play'])
    else:
        return False
