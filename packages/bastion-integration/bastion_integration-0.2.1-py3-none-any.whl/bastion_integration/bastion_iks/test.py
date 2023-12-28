# import json
#
# from loguru import logger
#
# from bastion_integration.bastion_iks.bastion_v2_dto import BastionV2Config
# from bastion_integration.bastion_iks.core import CoreV2
#
#
# bastion_v2_config = """
#                 {
#                     "server_config":
#                     {
#                         "host": "192.168.4.198",
#                         "port": 5005,
#                         "https": false
#                     },
#                     "operator_info":
#                     {
#                         "login": "q",
#                         "password": "q"
#                     },
#                     "enable_integration": true
#                 }
# """
# def main():
#     config = BastionV2Config(**json.loads(bastion_v2_config))
#     bastion = BastionV2(core=CoreV2, config=config)
#     bastion.init()
#
#     bastion.core.get_bastion_dict_values()
#
#
#
#
#
#
#
#
#
#
# if __name__ == "__main__":
#     main()
