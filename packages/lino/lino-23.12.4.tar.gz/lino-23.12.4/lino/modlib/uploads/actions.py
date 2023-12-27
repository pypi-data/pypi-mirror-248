# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import base64
from django.utils import timezone
from lino.api import rt, dd, _
from .mixins import make_captured_image


class CameraStream(dd.Action):
    """ Uses ImageCapture API to take images and videos through device camera """
    label = _("Camera")
    select_rows = False
    http_method = 'POST'
    button_text = "📷"  # U+1F4F7

    preprocessor = "Lino.captureImage"

    parameters = {
        "description": dd.CharField(_("Description"), max_length=200, blank=True),
        "type": dd.ForeignKey("uploads.UploadType", blank=True, null=True)
    }

    params_layout = """
    type
    description
    """

    def base64_to_image(self, imgstring):
        imgdata = base64.b64decode(imgstring.split('base64,')[1])
        return make_captured_image(imgdata, timezone.now())

    def run_from_ui(self, ar, **kwargs):
        file = self.base64_to_image(ar.request.POST['image'])
        upload = rt.models.uploads.Upload(file=file, user=ar.get_user(), **ar.action_param_values)
        upload.save_new_instance(ar)
        ar.goto_instance(upload)
