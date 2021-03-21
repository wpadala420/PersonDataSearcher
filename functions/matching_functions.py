from functions import image_functions


def match_profiles_by_photos(profile1, profile2):
    if len(profile1.facebook) > 0:
        if len(profile2.instagram) > 0:
            if 'profile_photo_path' in profile1.facebook and profile1.facebook['profile_photo_path'] is not None and profile1.facebook['profile_photo_path'] != '':
                if 'profile_photo_path' in profile2.instagram and profile2.instagram['profile_photo_path'] is not None and profile2.instagram['profile_photo_path'] != '':
                    if image_functions.compare_faces(profile1.facebook['profile_photo_path'], profile2.instagram['profile_photo_path']) is True:
                        return True
                if len(profile2.instagram['posts']) > 0:
                    for post in profile2.instagram['posts']:
                        if 'path' in post and post['path'] is not None and post['path'] != '':
                            if image_functions.compare_faces(profile1.facebook['profile_photo_url'], post['path']) is True:
                                return True
        if len(profile2.twitter) > 0:
            if 'profile_img_path' in profile2.twitter and profile2.twitter['profile_img_path'] is not None and profile2.twitter['profile_img_path'] != '':
                if 'profile_photo_path' in profile1.facebook and profile1.facebook['profile_photo_path'] is not None and profile1.facebook['profile_photo_path'] != '':
                    if image_functions.compare_faces(profile1.facebook['profile_photo_path'], profile2.twitter['profile_img_path']) is True:
                        return True
    if len(profile1.twitter) > 0:
        if 'profile_img_path' in profile1.twitter and profile1.twitter['profile_img_path'] is not None and profile1.twitter['profile_img_path'] != '':
            if len(profile2.instagram) > 0:
                if 'profile_photo_path' in profile2.instagram and profile2.instagram['profile_photo_path'] is not None and profile2.instagram['profile_photo_path'] != '':
                    if image_functions.compare_faces(profile1.twitter['profile_img_path'], profile2.instagram['profile_photo_path']) is True:
                        return True
                    if len(profile2.instagram['posts']) > 0:
                        for post in profile2.instagram['posts']:
                            if 'path' in post and post['path'] is not None and post['path'] != '':
                                if image_functions.compare_faces(profile1.twitter['profile_img_path'], post['path']) is True:
                                    return True
            if len(profile2.facebook) > 0:
                if 'profile_photo_path' in profile2.facebook and profile2.facebook['profile_photo_path'] is not None and profile2.facebook['profile_photo_path'] != '':
                    if image_functions.compare_faces(profile1.twitter['profile_img_path'], profile2.facebook['profile_photo_path']) is True:
                        return True
    if len(profile1.instagram) > 0:
        if len(profile2.twitter) > 0:
            if 'profile_img_path' in profile2.twitter and profile2.twitter['profile_img_path'] is not None and profile2.twitter['profile_img_path'] != '':
                if 'profile_photo_path' in profile1.instagram and profile1.instagram['profile_photo_path'] is not None and profile1.instagram['profile_photo_path'] != '':
                    if image_functions.compare_faces(profile1.instagram['profile_photo_path'], profile2.twitter['profile_img_path']) is True:
                        return True
                if len(profile1.instagram['posts']) > 0:
                    for post in profile1.instagram['posts']:
                        if 'path' in post and post['path'] is not None and post['path'] != '':
                            if image_functions.compare_faces(post['path'], profile2.twitter['profile_img_path']) is True:
                                return True
        if len(profile2.facebook) > 0:
            if 'profile_photo_path' in profile2.facebook and profile2.facebook['profile_photo_path'] is not None and profile2.facebook['profile_photo_path'] != '':
                if 'profile_photo_path' in profile1.instagram and profile1.instagram['profile_photo_path'] is not None and profile1.instagram['profile_photo_path'] != '':
                    if image_functions.compare_faces(profile1.instagram['profile_photo_path'], profile2.facebook['profile_photo_path']) is True:
                        return True
                if len(profile1.instagram['posts']) > 0:
                    for post in profile1.instagram['posts']:
                        if 'path' in post and post['path'] is not None and post['path'] != '':
                            if image_functions.compare_faces(post['path'], profile2.facebook['profile_photo_path']) is True:
                                return True
    return False



