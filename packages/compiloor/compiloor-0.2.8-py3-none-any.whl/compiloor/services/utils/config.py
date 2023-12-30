from json import dumps

from os import makedirs
from os.path import expanduser, isdir, isfile, join

from compiloor.constants.environment import (
    BASE_CONFIG_SCHEMA,
    COMPILOOR_CACHE_DIRECTORY,
    CONFIG_NAME,
    CONFIG_SECTION_DEFAULT
)

from compiloor.services.logger.logger import Logger
from compiloor.services.typings.config import ConfigSection
from compiloor.services.utils.utils import validate_url


class ConfigUtils:
    """
        Miscellaneous functions for the configuration file.
    """
    
    # @audit Do we need a whole utility class for one static method?
    
    @staticmethod
    def validate_config_template_urls(config: dict) -> None:
        # Checking whether the keys are present:
        template_url_is_valid: bool = "template_url" in config         
        stylesheet_url_is_valid: bool = "stylesheet_url" in config
        
        # Checking whether the URLs are valid:
        if stylesheet_url_is_valid: stylesheet_url_is_valid = validate_url(config["stylesheet_url"])
        if template_url_is_valid: template_url_is_valid = validate_url(config["template_url"])

        if not template_url_is_valid and not stylesheet_url_is_valid:
            Logger.error("The template URL and the stylesheet URL must be valid URLs.")
            exit(1)
            
        if not template_url_is_valid:
            Logger.error("The template URL must be a valid URL.")
            exit(1)
            
        if not stylesheet_url_is_valid:
            Logger.error("The stylesheet URL must be a valid URL.")
            exit(1)
    
    @staticmethod
    def get_global_config_location() -> str:
        """
            Returns the location of the base config.
        """
        return join(
            expanduser('~'),
            '.cache',
            COMPILOOR_CACHE_DIRECTORY,
            CONFIG_NAME
        )
    
    @staticmethod
    def mutate_global_config(config: dict | str = BASE_CONFIG_SCHEMA, should_emit_log: bool = True) -> None:
        """
            Creates a default configuration file in the package root.
        """

        if isinstance(config, dict): config = dumps(config, indent=4)
        elif isfile(config): config = open(config).read()
        else: config = dumps(BASE_CONFIG_SCHEMA, indent=4)
        
        global_config_src: str = ConfigUtils.get_global_config_location()

        package_dir: str = global_config_src.replace(CONFIG_NAME, "")

        if not isfile(global_config_src):
            makedirs(package_dir.replace(CONFIG_NAME, ""))

        open(global_config_src, "w").write(config)
        
        if not should_emit_log: return 

        Logger.success(f"Successfully mutated the default config!")
        
    @staticmethod
    def mutate_global_config_section(section_name: ConfigSection, src: str = CONFIG_SECTION_DEFAULT, should_emit_log: bool = True) -> None:
        """
            Mutates a specific section of the global config.
        """
        global_config_src: str = ConfigUtils.get_global_config_location().replace(CONFIG_NAME, "")
        sections_src: str = join(global_config_src, "sections")
        
        if not isdir(sections_src):
            makedirs(sections_src)
        
        if isfile(src): src = open(src).read()
        elif not src: src = CONFIG_SECTION_DEFAULT
        elif not isinstance(src, str): src = str(src) 
        
        current_section_src: str = join(sections_src, f"{section_name.value}_content.md")
        
        open(current_section_src, "w").write(src)
        
        if not should_emit_log: return
        
        Logger.success(f'Successfully mutated the "{section_name.value}" section!')
        
        