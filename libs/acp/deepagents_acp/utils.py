from acp.schema import (
    AudioContentBlock,
    EmbeddedResourceContentBlock,
    ImageContentBlock,
    ResourceContentBlock,
    TextContentBlock,
)


def convert_text_block_to_content_blocks(block: TextContentBlock):
    return [{"type": "text", "text": block.text}]


def convert_image_block_to_content_blocks(block: ImageContentBlock):
    # Image blocks contain visual data
    # Primary case: inline base64 data (data is already a base64 string)
    if block.data:
        data_uri = f"data:{block.mime_type};base64,{block.data}"
        return [{"type": "image_url", "image_url": {"url": data_uri}}]

    # No data available
    return [{"type": "text", "text": "[Image: no data available]"}]


def convert_audio_block_to_content_blocks(block: AudioContentBlock):
    raise Exception("Audio is not currently supported.")


def convert_resource_block_to_content_blocks(block: ResourceContentBlock):
    # Resource blocks reference external resources with absolute paths
    resource_text = f"[Resource: {block.name}"
    if block.uri:
        resource_text += f"\nURI: {block.uri}"
    if block.description:
        resource_text += f"\nDescription: {block.description}"
    if block.mime_type:
        resource_text += f"\nMIME type: {block.mime_type}"
    resource_text += "]"
    return [{"type": "text", "text": resource_text}]


def convert_embedded_resource_block_to_content_blocks(
    block: EmbeddedResourceContentBlock,
) -> list[dict]:
    # Embedded resource blocks contain the resource data inline
    resource = block.resource
    if hasattr(resource, "text"):
        mime_type = getattr(resource, "mime_type", "application/text")
        return [{"type": "text", "text": f"[Embedded {mime_type} resource: {resource.text}"}]
    elif hasattr(resource, "blob"):
        mime_type = getattr(resource, "mime_type", "application/octet-stream")
        data_uri = f"data:{mime_type};base64,{resource.blob}"
        return [
            {
                "type": "text",
                "text": f"[Embedded resource: {data_uri}]",
            }
        ]
    else:
        raise Exception(
            "Could not parse embedded resource block. "
            "Block expected either a `text` or `blob` property."
        )
