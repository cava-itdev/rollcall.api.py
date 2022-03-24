# Rollcall API

## Overview
* The API attempts to recognise a known member from a photo.
* Members' attendances at meetings are recorded.

## Mechanism
* _identifyMember_ is called, supplying a frontal face photo as a Base64 string.
* First, the API attempts to detect a face in the photo (using OpenCV).
* If a face is detected, the photo is stored in a staging folder with a unique ID.
* Then an attempt is made to identify the member from existing photos of known members.
* If the member is successfully identified, the member's ID and name is returned for verification together with the photo ID.
* _registerMember_ is called, supplying a member ID and the photo ID. This will record the member's attendance and move the photo to the member's folder for future use.