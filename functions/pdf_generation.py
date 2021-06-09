from fpdf import FPDF


class PDFReport(FPDF):

    def __init__(self, profile):
        super().__init__()
        self.profile = profile

    def header(self):
        if self.page > 1:
            return
        self.set_doc_option('core_fonts_encoding', 'utf-8')
        self.add_font('DejaVuB', '', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf', uni=True)
        self.set_font('DejaVuB', '', 18)
        name = ''
        surname = ''
        if self.profile.name == '' and self.profile.surname == '':
            if len(self.profile.facebook) > 0:
                if self.profile.facebook['name'] != '':
                    name = self.profile.facebook['name']
                if self.profile.facebook['surname'] != '':
                    surname = self.profile.facebook['surname']
        else:
            name = self.profile.name
            surname = self.profile.surname

        if 'profile_photo_path' in self.profile.facebook and self.profile.facebook['profile_photo_path'] != '':
            self.image(self.profile.facebook['profile_photo_path'], 10, 8, 33)
        elif 'profile_img_path' in self.profile.twitter and self.profile.twitter['profile_img_path'] != '':
            self.image(self.profile.twitter['profile_img_path'], 10, 8, 33)
        elif 'profile_photo_path' in self.profile.instagram and self.profile.instagram['profile_photo_path'] != '':
            self.image(self.profile.instagram['profile_photo_path'], 10, 8, 33)
        # self.set_font('Arial', 'B', 18)

        self.cell(100)
        self.cell(0, 5, (name + ' ' + surname), ln=1)
        self.ln(60)

    def create(self, path):
        self.set_doc_option('core_fonts_encoding', 'utf-8')
        self.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 10)
        self.alias_nb_pages()
        self.add_page()
        # self.set_font('Arial', '', 12)
        if len(self.profile.facebook) > 0:
            fb_title = 'FACEBOOK'
            self.cell(0, 5, fb_title, ln=1, align='C')
            self.cell(0, 5, ('Username: ' + self.profile.facebook['username']), ln=1)
            if len(self.profile.facebook['living_places']) > 0:
                self.cell(0, 5, 'Miejsca:', ln=1)
                for place in self.profile.facebook['living_places']:
                    place_line = ''
                    for key in place:
                        place_line = key + ' - ' + place[key]
                        self.cell(0, 5, place_line, ln=1)
            if len(self.profile.facebook['education']) > 0:
                self.cell(0, 5, 'Edukacja:', ln=1)
                for ed in self.profile.facebook['education']:
                    e_line = str(ed)
                    self.cell(0, 5, e_line, ln=1)
            if len(self.profile.facebook['relationship']) > 0:
                self.cell(0, 5, 'Zwiazki:', ln=1)
                for r in self.profile.facebook['relationship']:
                    r_line = ''
                    for rk in r:
                        r_line = r_line + rk + ' - ' + r[rk]
                    self.cell(0, 5, r_line, ln=1)
            if len(self.profile.facebook['photos_paths']) > 0:
                self.cell(0, 5, 'Zdjecia:', ln=1)
                for photo in self.profile.facebook['photos_paths']:
                    self.image(photo, 100)
            if len(self.profile.facebook['friends']) > 0:
                self.cell(0, 5, 'Znajomi:', ln=1)
                for friend in self.profile.facebook['friends']:
                    self.cell(0, 5, friend, ln=1)
            if len(self.profile.fb_username_related_accounts) > 0:
                self.cell(0, 5, 'Konta na innych serwisach powiazane z nazwa uzytkownika z facebooka:', ln=1)
                for acc in self.profile.fb_username_related_accounts:
                    acc_line = acc['site_name'] + ' - ' + acc['site_url']
                    self.cell(0, 5, acc_line, ln=1)
        if len(self.profile.twitter) > 0:
            self.cell(0, 5, 'TWITTER', ln=1, align='C')
            self.cell(0, 5, self.profile.twitter['url'], ln=1)
            self.cell(0, 5, 'Username: ' + self.profile.twitter['nickname'], ln=1)
            if self.profile.twitter['profile_img_path'] != '':
                self.cell(0, 5, 'Zdjecie profilowe:', ln=1)
                self.image(self.profile.twitter['profile_img_path'], 75)
            if 'role' in self.profile.twitter:
                self.multi_cell(0, 5, self.profile.twitter['role'])
                self.ln(20)
            if len(self.profile.twitter['sites']) > 0:
                self.cell(0, 5, 'Powiazane strony:', ln=1)
                for site in self.profile.twitter['sites']:
                    self.cell(0, 5, site, ln=1)
            if self.profile.twitter['report'] != '':
                with open(self.profile.twitter['report'], 'rb') as t_report:
                    for lt in t_report:
                        new_line = str(lt, encoding='utf-8')
                        self.cell(0, 5, new_line, ln=1)
            if 'hashtags' in self.profile.twitter and len(self.profile.twitter['hashtags']) > 0:
                self.cell(0, 5, 'Najczesciej uzywane hashtagi:', ln=1)
                for ht in self.profile.twitter['hashtags']:
                    self.cell(0, 5, ht, ln=1)
            if len(self.profile.twitter_username_connected_profiles) > 0:
                self.cell(0, 5, 'Konta na innych serwisach powiazane z nazwa uzytkownika z twittera:', ln=1)
                for acc in self.profile.twitter_username_connected_profiles:
                    acc_line = acc['site_name'] + ' - ' + acc['site_url']
                    self.cell(0, 5, acc_line, ln=1)
        if len(self.profile.instagram) > 0:
            self.cell(0, 5, 'INSTAGRAM', ln=1, align='C')
            self.cell(0, 5, self.profile.instagram['url'], ln=1)
            self.cell(0, 5, 'Username: ' + self.profile.instagram['login'], ln=1)
            if self.profile.instagram['profile_photo_path'] != '':
                self.cell(0, 5, 'Zdjecie profilowe:', ln=1)
                self.image(self.profile.instagram['profile_photo_path'], 100)
            if len(self.profile.instagram['posts']) > 0:
                self.cell(0, 5, 'Zdjecia:', ln=1)
                connected_people = []
                for post in self.profile.instagram['posts']:
                    if post['path'] != '':
                        self.image(post['path'], 100)
                        for tagged_user in post['users tagged']:
                            connected_people.append(tagged_user)
                connected_people = set(connected_people)
                if len(connected_people) > 0:
                    self.cell(0, 5, 'Oznaczani uzytkownicy:', ln=1)
                    for user in connected_people:
                        self.cell(0, 5, user, ln=1)
            if len(self.profile.instagram_username_related_profiles) > 0:
                self.cell(0, 5, 'Konta na innych serwisach powiazane z nazwa uzytkownika z Instagrama:', ln=1)
                for acc in self.profile.instagram_username_related_profiles:
                    acc_line = acc['site_name'] + ' - ' + acc['site_url']
                    self.cell(0, 5, acc_line, ln=1)
        if len(self.profile.registries) > 0:
            self.cell(0, 5, 'KRS', ln=1, align='C')
            for reg in self.profile.registries:
                if len(reg['organizations_data']) > 0:
                    for o_data in reg['organizations_data']:
                        self.cell(0, 5, 'Nazwa firmy: ' + o_data['name'], ln=1)
                        self.cell(0, 5, 'REGON: ' + o_data['regon'], ln=1)
                        self.cell(0, 5, 'NIP: ' + o_data['nip'], ln=1)
                        self.cell(0, 5, 'Budzet: ' + str(o_data['stock']), ln=1)
                        if len(o_data['address']) > 0:
                            adr = o_data['address']['street'] + ' ' + o_data['address']['house_no'] + ', ' + o_data['address']['code'] + ' ' + o_data['address']['post_office']
                            adr_line = 'Adres: ' + adr
                            self.cell(0, 5, adr_line, ln=1)
                        if len(o_data['ceo']) > 0:
                            self.cell(0, 5, 'CEO:', ln=1)
                            self.cell(0, 5, o_data['ceo']['full_name'], ln=1)
                            self.cell(0, 5, o_data['ceo']['birthday'], ln=1)
                            self.cell(0, 5, o_data['ceo']['title'], ln=1)
        if len(self.profile.vindicat_data) > 0:
            self.cell(0, 5, 'DŁUGI', ln=1, align='C')
            for vd in self.profile.vindicat_data:
                amount_line = 'KWOTA: ' + vd['debts_sum']
                details_line = 'SZCZEGOŁY: ' + 'https://vindicat.pl' + vd['site_details']
                self.cell(0, 5, amount_line, ln=1)
                self.cell(0, 5, details_line, ln=1)
        self.output(path)
