# devops-netology

 - devops-netology.gitignore - исключает каталог с его содержимым .idea/ .
 - devops-netology/terraform/.gitignore - исключает из версионирования
указанные в нём файлы и файлы подходящие под указанные маски. 

 - **/.terraform/* игнорируются все локальные директории с именем .terraform и их содержимое
 - *.tfstate игнорируются файлы с расширением .tfstate
 - *.tfstate.* игнорируются файлы содержащие в имени ".tfstate."
 - crash.log этот файл игнорируется
 - crash.*.log игнорируются файлы начинающиеся на "crash." и заканчивающиеся на ".log"
 - *.tfvars игнорируются файлы с расширением .tfvars
 - override.tf этот файл игнорируется
 - override.tf.json этот файл игнорируется
 - *_override.tf игнорируются фалы заканчивающиеся на "_override.tf"
 - *_override.tf.json игнорируются фалы заканчивающиеся на "_override.tf"
 - .terraformrc этот файл игнорируется
 - terraform.rc этот файл игнорируется