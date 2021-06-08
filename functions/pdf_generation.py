from fpdf import FPDF


class PDFReport(FPDF):

    def __init__(self, profile):
        super().__init__()
        self.profile = profile

    def header(self):
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
        elif self.profile.twitter['profile_img_path'] != '':
            self.image(self.profile.twitter['profile_img_path'], 10, 8, 33)
        elif self.profile.instagram['profile_photo_path'] != '':
            self.image(self.profile.instagram['profile_photo_path'], 10, 8, 33)
        self.set_font('Arial', 'B', 18)
        self.cell(100)
        self.cell(0, 5, name + ' ' + surname, ln=1)
        self.ln(30)

    def create(self, path):
        self.alias_nb_pages()
        self.add_page()
        self.set_font('Times', '', 14)
        if len(self.profile.facebook) > 0:
            fb_title = 'FACEBOOK'
            self.cell(0, 5, fb_title, ln=1, align='C')
            self.cell(0, 5, 'Nazwa użytkownika: ' + self.profile.facebook['username'], ln=1)
            if len(self.profile.facebook['living_places']) > 0:
                self.cell(0, 5, 'Miejsca:', ln=1)
                for place in self.profile.facebook['living_places']:
                    place_line = ''
                    for key in place:
                        place_line = '\t' + key + ' - ' + place[key]
                        self.cell(0, 5, place_line, ln=1)
            if len(self.profile.facebook['education']) > 0:
                self.cell(0, 5, 'Edukacja:', ln=1)
                for ed in self.profile.facebook['education']:
                    e_line = '\t' + str(ed)
                    self.cell(0, 5, e_line, ln=1)
            if len(self.profile.facebook['relationship']) > 0:
                self.cell(0, 5, 'Związki:', ln=1)
                for r in self.profile.facebook['relationship']:
                    r_line = ''
                    for rk in r:
                        r_line = '\t' + r_line + rk + ' - ' + r[rk]
                    self.cell(0, 5, r_line, ln=1)
            if len(self.profile.facebook['photos_paths']) > 0:
                self.cell(0, 5, 'Zdjęcia:', ln=1)
                for photo in self.profile.facebook['photos_paths']:
                    self.image(photo, 100)
            if len(self.profile.facebook['friends']) > 0:
                self.cell(0, 5, 'Znajomi:', ln=1)
                for friend in self.profile.facebook['friends']:
                    self.cell(0, 5, '\t' + friend, ln=1)
            if len(self.profile.fb_username_related_accounts) > 0:
                self.cell(0, 5, 'Konta na innych serwisach powiązane z nazwą użytkownika z facebooka:', ln=1)
                for acc in self.profile.fb_username_related_accounts:
                    acc_line = '\t' + acc['site_name'] + ' - ' + acc['site_url']
                    self.cell(0, 5, acc_line, ln=1)
        if len(self.profile.twitter) > 0:
            self.cell(0, 5, 'TWITTER', ln=1, align='C')
            self.cell(0, 5, self.profile.twitter['url'], ln=1)
            self.cell(0, 5, 'Nazwa użytkownika: ' + self.profile.twitter['nickname'], ln=1)
            if self.profile.twitter['profile_img_path'] != '':
                self.cell(0, 5, 'Zdjęcie profilowe:', ln=1)
                self.image(self.profile.twitter['profile_img_path'], 75)
            if 'role' in self.profile.twitter:
                self.cell(0, 5, self.profile.twitter['role'], ln=1)
            if len(self.profile.twitter['sites']) > 0:
                self.cell(0, 5, 'Powiązane strony:', ln=1)
                for site in self.profile.twitter['sites']:
                    self.cell(0, 5, '\t' + site, ln=1)
            if self.profile.twitter['report'] != '':
                with open(self.profile.twitter['report'], 'rb') as t_report:
                    for lt in t_report:
                        new_line = str(lt, encoding='utf-8')
                        self.cell(0, 5, new_line, ln=1)
            if 'hashtags' in self.profile.twitter and len(self.profile.twitter['hashtags']) > 0:
                self.cell(0, 5, 'Najczęściej używane hashtagi:', ln=1)
                for ht in self.profile.twitter['hashtags']:
                    self.cell(0, 5, '\t' + ht, ln=1)
            if len(self.profile.twitter_username_connected_profiles) > 0:
                self.cell(0, 5, 'Konta na innych serwisach powiązane z nazwą użytkownika z twittera:', ln=1)
                for acc in self.profile.twitter_username_connected_profiles:
                    acc_line = '\t' + acc['site_name'] + ' - ' + acc['site_url']
                    self.cell(0, 5, acc_line, ln=1)
        if len(self.profile.instagram) > 0:
            self.cell(0, 5, 'INSTAGRAM', ln=1, align='C')
            self.cell(0, 5, self.profile.instagram['url'], ln=1)
            self.cell(0, 5, 'Nazwa użytkownika: ' + self.profile.instagram['login'], ln=1)
            if self.profile.instagram['profile_photo_path'] != '':
                self.cell(0, 5, 'Zdjęcie profilowe:', ln=1)
                self.image(self.profile.instagram['profile_photo_path'], 100)
            if len(self.profile.instagram['posts']) > 0:
                self.cell(0, 5, 'Zdjęcia:', ln=1)
                connected_people = []
                for post in self.profile.instagram['posts']:
                    if post['path'] != '':
                        self.image(post['path'], 100)
                        for tagged_user in post['users tagged']:
                            connected_people.append(tagged_user)
                connected_people = set(connected_people)
                if len(connected_people) > 0:
                    self.cell(0, 5, 'Oznaczani użytkownicy:', ln=1)
                    for user in connected_people:
                        self.cell(0, 5, '\t' + user, ln=1)
            if len(self.profile.instagram_username_related_profiles) > 0:
                self.cell(0, 5, 'Konta na innych serwisach powiązane z nazwą użytkownika z Instagrama:', ln=1)
                for acc in self.profile.instagram_username_related_profiles:
                    acc_line = '\t' + acc['site_name'] + ' - ' + acc['site_url']
                    self.cell(0, 5, acc_line, ln=1)
        if len(self.profile.registries) > 0:
            self.cell(0, 5, 'KRS', ln=1, align='C')
            for reg in self.profile.registries:
                if len(reg['organizations_data']) > 0:
                    for o_data in reg['organizations_data']:
                        self.cell(0, 5, 'Nazwa firmy: ' + o_data['name'], ln=1)
                        self.cell(0, 5, 'REGON: ' + o_data['regon'], ln=1)
                        self.cell(0, 5, 'NIP: ' + o_data['nip'], ln=1)
                        self.cell(0, 5, 'Budżet: ' + str(o_data['stock']), ln=1)
                        if len(o_data['address']) > 0:
                            adr = o_data['address']['street'] + ' ' + o_data['address']['house_no'] + ', ' + o_data['address']['code'] + ' ' + o_data['address']['post_office']
                            adr_line = 'Adres: ' + adr
                            self.cell(0, 5, adr_line, ln=1)
                        if len(o_data['ceo']) > 0:
                            self.cell(0, 5, 'CEO:', ln=1)
                            self.cell(0, 5, '\t' + o_data['ceo']['full_name'], ln=1)
                            self.cell(0, 5, '\t' + o_data['ceo']['birthday'], ln=1)
                            self.cell(0, 5, '\t' + o_data['ceo']['title'], ln=1)
        if len(self.profile.vindicat_data) > 0:
            self.cell(0, 5, 'DŁUGI', ln=1, align='C')
            for vd in self.profile.vindicat_data:
                amount_line = 'KWOTA: ' + vd['debts_sum']
                details_line = 'SZCZEGÓŁY: ' + 'https://vindicat.pl' + vd['site_details']
                self.cell(0, 5, amount_line, ln=1)
                self.cell(0, 5, details_line, ln=1)
        self.output(path)
