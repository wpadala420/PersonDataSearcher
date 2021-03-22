import os

def generate_raport(directory, filename, profile):
    if os.path.isdir(directory) is False:
        os.mkdir(directory)
    path = directory + '/' + filename
    with open(path, 'wb') as raport:
        name = ''
        surname = ''
        if profile.name == '' and profile.surname == '':
            if len(profile.facebook) > 0:
                if profile.facebook['name'] != '':
                    name = profile.facebook['name']
                if profile.facebook['surname'] != '':
                    surname = profile.facebook['surname']
        else:
            name = profile.name
            surname = profile.surname
        name_line = 'Imię i nazwisko: ' + name + ' ' + surname + '\n'
        raport.write(bytes(name_line, encoding='utf-8'))
        bith_line = 'Data urodzenia: ' + profile.dateOfBirth + '\n'
        raport.write(bytes(bith_line, encoding='utf-8'))
        facebook_header = 'Dane z Facebooka:' + '\n'
        raport.write(bytes(facebook_header, encoding='utf-8'))
        if len(profile.facebook) > 0:
            fb_username = 'Nazwa użytkownika: ' + profile.facebook['username'] + '\n'
            raport.write(bytes(fb_username, encoding='utf-8'))
            fb_friends = 'Znajomi:' + '\n'
            raport.write(bytes(fb_friends, encoding='utf-8'))
            for friend in profile.facebook['friends']:
                raport.write(bytes('\t' + friend + '\n', encoding='utf-8'))

            if 'profile_photo_path' in profile.facebook and profile.facebook['profile_photo_path'] != '':
                profile_photo = 'Lokalizacja pobranego zdjęcia profilowego: ' + profile.facebook['profile_photo_path'] + '\n'
                raport.write(bytes(profile_photo, encoding='utf-8'))

            if len(profile.facebook['photos_paths']) > 0:
                photos = 'Zdjęcia:' + '\n'
                raport.write(bytes(photos, encoding='utf-8'))
                for photo in profile.facebook['photos_paths']:
                    photo_line = '\t lokalizacja: ' + photo + '\n'
                    raport.write(bytes(photo_line, encoding='utf-8'))
            if len(profile.facebook['living_places']) > 0:
                places = 'Miejsca:' + '\n'
                raport.write(bytes(places, encoding='utf-8'))
                for place in profile.facebook['living_places']:
                    line = '\t' + str(place) + '\n'
                    raport.write(bytes(line, encoding='utf-8'))

            if len(profile.facebook['education']) > 0:
                edu = 'Edukacja:' + '\n'
                raport.write(bytes(edu, encoding='utf-8'))
                for ed in profile.facebook['education']:
                    e_line = '\t' + str(ed) + '\n'
                    raport.write(bytes(e_line, encoding='utf-8'))

            if len(profile.facebook['relationship']) > 0:
                relat = 'Związki:' + '\n'
                raport.write(bytes(relat, encoding='utf-8'))
                for r in profile.facebook['relationship']:
                    r_line = '\t' + str(r) + '\n'
                    raport.write(bytes(r_line, encoding='utf-8'))


        if len(profile.twitter) > 0:
            twitter_header = 'Dane z Twittera:' + '\n'
            raport.write(bytes(twitter_header, encoding='utf-8'))
            t_username = 'Nazwa użytkownika: ' + profile.twitter['nickname'] + '\n'
            raport.write(bytes(t_username, encoding='utf-8'))
            if 'role' in profile.twitter:
                raport.write(bytes(profile.twitter['role'] + '\n', encoding='utf-8'))
            u_line = 'URL: ' + profile.twitter['url'] + '\n'
            raport.write(bytes(u_line, encoding='utf-8'))
            if len(profile.twitter['sites']) > 0:
                sites = 'Powiązane strony:' + '\n'
                raport.write(bytes(sites, encoding='utf-8'))
                for site in profile.twitter['sites']:
                    s_line = '\t' + site + '\n'
                    raport.write(bytes(s_line, encoding='utf-8'))
            if profile.twitter['profile_img_path'] != '':
                tt_pp = 'Lokalizacja zdjęcia profilowego:' + '\n'
                raport.write(bytes(tt_pp, encoding='utf-8'))
                tt_pp_p = '\t' + profile.twitter['profile_img_path'] + '\n'
                raport.write(bytes(tt_pp_p, encoding='utf-8'))
            if profile.twitter['report'] != '':
                tr = 'Analiza Tweetów' + '\n'
                raport.write(bytes(tr, encoding='utf-8'))
                with open(' ' + profile.twitter['report'], 'rb') as t_report:
                    for lt in t_report:
                        new_line = '\t' + str(lt, encoding='utf-8')
                        raport.write(bytes(new_line, encoding='utf-8'))

        if len(profile.instagram) > 0:
            ig_header = 'Dane z Instagrama:' + '\n'
            raport.write(bytes(ig_header, encoding='utf-8'))
            ig_login = 'Nazwa uzytkownika: ' + profile.instagram['login'] + '\n'
            raport.write(bytes(ig_login, encoding='utf-8'))
            url_val = 'URL: ' + profile.instagram['url'] + '\n'
            raport.write(bytes(url_val, encoding='utf-8'))
            if profile.instagram['profile_photo_path'] != '':
                ig_pp = 'Lokalizacja zdjęcia profilowego: ' + profile.instagram['profile_photo_path'] + '\n'
                raport.write(bytes(ig_pp, encoding='utf-8'))
            if len(profile.instagram['posts']) > 0:
                ig_ps = 'Zdjęcia:' + '\n'
                raport.write(bytes(ig_ps, encoding='utf-8'))
                for post in profile.instagram['posts']:
                    if post['path'] != '':
                        raport.write(bytes('\t' + post['path'] + '\n', encoding='utf-8'))


        if len(profile.registries) > 0:
            reg_header = 'Dane z KRS:' + '\n'
            raport.write(bytes(reg_header, encoding='utf-8'))
            for reg in profile.registries:
                if len(reg['organizations_data']) > 0:
                    for o_data in reg['organizations_data']:
                        comp_name = 'Nazwa firmy:' + o_data['name'] + '\n'
                        raport.write(bytes('\t' + comp_name, encoding='utf-8'))
                        regon = 'REGON: ' + o_data['regon'] + '\n'
                        nip = 'NIP: ' + o_data['nip'] + '\n'
                        raport.write(bytes('\t' + regon, encoding='utf-8'))
                        raport.write(bytes('\t' + nip, encoding='utf-8'))
                        stock = 'Budżet: ' + str(o_data['stock']) + '\n'
                        raport.write(bytes('\t' +stock, encoding='utf-8'))
                        if len(o_data['address']) > 0:
                            adr = o_data['address']['street'] + ' ' + o_data['address']['house_no'] + ', ' + o_data['address']['code'] + ' ' + o_data['address']['post_office']
                            adr_line = 'Adres: ' + adr + '\n'
                            raport.write(bytes('\t' + adr_line, encoding='utf-8'))
                        if len(o_data['ceo']) > 0:
                            ceo_line = "CEO:" + '\n'
                            raport.write(bytes('\t' + ceo_line, encoding='utf-8'))
                            raport.write(bytes('\t\t' + o_data['ceo']['full_name'] + '\n', encoding='utf-8'))
                            raport.write(bytes('\t\t' + o_data['ceo']['birthday'] + '\n', encoding='utf-8'))
                            raport.write(bytes('\t\t' + o_data['ceo']['title'] + '\n', encoding='utf-8'))





