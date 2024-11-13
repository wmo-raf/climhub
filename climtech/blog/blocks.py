from climtech.core.blocks import StandaloneCTABlock
from climtech.utils.blocks import StoryBlock


class BlogStoryBlock(StoryBlock):
    standalone_cta = StandaloneCTABlock(group="CTA options")
