import cloudinary.uploader


def upload_image(validated_data):
    result = cloudinary.uploader.upload(
        validated_data['image'], folder=validated_data['folder'], resource_type='image'
    )
    if not result.get('secure_url') or not result.get('public_id'):
        raise ValueError('The media provider did not confirm the upload.')
    return {key: result.get(key) for key in ('secure_url', 'public_id', 'format', 'bytes')}
