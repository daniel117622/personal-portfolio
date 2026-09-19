from enum import Enum

class _CallableStringEnum(str, Enum):
    def __call__(self):
        return self.value
    
class ValidCategories(_CallableStringEnum):
    HOME              = "Home"
    CV                = "CV"
    WORK_EXPERIENCE   = "Work Experience"
    ACTIVE_PROJECTS   = "Active Projects"
    GITHUB_PROJECTS   = "GitHub Projects"
    OLD_PROJECTS      = "Old Projects"
    EXPERIMENTAL_TECH = "Experimental Tech"
    RESEARCH          = "Research"
    DEVLOG            = "Devlog"
    ARTICLES          = "Articles"