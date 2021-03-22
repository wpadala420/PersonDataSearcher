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
        name_line = 'Imię i nazwisko: ' + name + ' ' + surname
        raport.write(name_line)
        bith_line = 'Data urodzenia: ' + profile.dateOfBirth
        raport.write(bith_line)
        facebook_header = 'Dane z Facebooka:'
        raport.write(facebook_header)
        if len(profile.facebook) > 0:
            fb_username = 'Nazwa użytkownika: ' + profile.facebook['username']
            raport.write(fb_username)
            fb_friends = 'Znajomi:'
            raport.write(fb_friends)
            for friend in profile.facebook['friends']:
                raport.write('\t' + friend)

            if profile.facebook['profile_photo_path'] != '':
                profile_photo = 'Lokalizacja pobranego zdjęcia profilowego: ' + profile.facebook['profile_photo_path']
                raport.write(profile_photo)

            if len(profile.facebook['photos_paths']) > 0:
                photos = 'Zdjęcia:'
                raport.write(photos)
                for photo in profile.facebook['photos_paths']:
                    photo_line = '\t lokalizacja: ' + photo
                    raport.write(photo_line)
            if len(profile.facebook['living_places']) > 0:
                places = 'Miejsca:'
                raport.write(places)
                for place in profile.facebook['living_places']:
                    line = '\t' + str(place)
                    raport.write(line)

            if len(profile.facebook['education']) > 0:
                edu = 'Edukacja:'
                raport.write(edu)
                for ed in profile.facebook['education']:
                    e_line = '\t' + str(ed)
                    raport.write(e_line)

            if len(profile.facebook['relationship']) > 0:
                relat = 'Związki:'
                raport.write(relat)
                for r in profile.facebook['relationship']:
                    r_line = '\t' + str(r)
                    raport.write(r_line)


        if len(profile.twitter) > 0:
            twitter_header = 'Dane z Twittera:'
            raport.write(twitter_header)
            t_username = 'Nazwa użytkownika: ' + profile.twitter['nickname']
            raport.write(t_username)
            raport.write(profile.twitter['role'])
            u_line = 'URL: ' + profile.twitter['url']
            raport.write(u_line)
            if len(profile.twitter['sites']) > 0:
                sites = 'Powiązane strony:'
                raport.write(sites)
                for site in profile.twitter['sites']:
                    s_line = '\t' + site
                    raport.write(s_line)
            if profile.twitter['profile_img_path'] != '':
                tt_pp = 'Lokalizacja zdjęcia profilowego:'
                raport.write(tt_pp)
                tt_pp_p = '\t' + profile.twitter['profile_img_path']
                raport.write(tt_pp_p)
            if profile.twitter['report'] != '':
                tr = 'Analiza Tweetów'
                raport.write(tr)
                with open(profile.twitter['report'], 'rb') as t_report:
                    for lt in t_report:
                        new_line = '\t' + lt
                        raport.write(new_line)

        if len(profile.instagram) > 0:
            ig_header = 'Dane z Instagrama:'
            raport.write(ig_header)
            ig_login = 'Nazwa uzytkownika: ' + profile.instagram['login']
            raport.write(ig_login)
            url_val = 'URL: ' + profile.instagram['url']
            if profile.instagram['profile_photo_path'] != '':
                ig_pp = 'Lokalizacja zdjęcia profilowego: ' + profile.instagram['profile_photo_path']
                raport.write(ig_pp)
            if len(profile.instagram['posts']) > 0:
                ig_ps = 'Zdjęcia:'
                raport.write(ig_ps)
                for post in profile.instagram['posts']:
                    if post['path'] != '':
                        raport.write('\t' + post['path'])


        if len(profile.registries) > 0:
            reg_header = 'Dane z KRS:'
            raport.write(reg_header)
            for reg in profile.registries:
                if len(reg['organizations_data']) > 0:
                    for o_data in reg['organizations_data']:
                        comp_name = 'Nazwa firmy:' + o_data['name']
                        raport.write('\t' + comp_name)
                        regon = 'REGON: ' + o_data['regon']
                        nip = 'NIP: ' + o_data['nip']
                        raport.write('\t' + regon)
                        raport.write('\t' + nip)
                        stock = 'Budżet: ' + o_data['stock']
                        raport.write( '\t' +stock)
                        if len(o_data['address']) > 0:
                            adr = o_data['address']['street'] + ' ' + o_data['address']['house_no'] + ', ' + o_data['address']['code'] + ' ' + o_data['address']['post_office']
                            adr_line = 'Adres: ' + adr
                            raport.write('\t' + adr_line)
                        if len(o_data['ceo']) > 0:
                            ceo_line = "CEO:"
                            raport.write('\t' + ceo_line)
                            raport.write('\t\t' + o_data['ceo']['full_name'])
                            raport.write('\t\t' + o_data['ceo']['birthday'])
                            raport.write('\t\t' + o_data['ceo']['title'])





