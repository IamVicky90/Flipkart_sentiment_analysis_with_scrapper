from datetime import datetime
import os
class log:
    def __init__(self):
        pass
    def log_writter(self,message,filename,message_type='INFO',create_log_for='t'):
        """
        params:
            - message: To write any message that you want
            - message_type: Press type of the message any type you want eg: 'INFO','ERROR','WARNING'
            - create_log_for: type 't' to create logs for training services or create 'p' for prediction service
        Written By: vicky
        Version: 1.0
        Revisions: None
        """
        os.makedirs(os.path.join(os.getcwd(),'Loggings'), exist_ok=True)
        absolute_path=os.path.join(os.getcwd(),'Loggings')
        if create_log_for=='t':
            os.makedirs(os.path.join(absolute_path,'Training_logs'),exist_ok=True)
            directory='Training_logs'
        elif create_log_for=='p':
            os.makedirs(os.path.join(absolute_path,'Prediction_logs'),exist_ok=True)
            directory='Prediction_logs'
        else:
            raise Exception("Invalid Argument: create_log_for\n\tExpected arguments are 't','p'")
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")
        file_path =os.path.join(absolute_path,directory,filename)
        with open(file_path,'a+') as f:
            f.write(str(self.now)+'\t'+str(self.date)+'\t\t'+str(message_type)+': '+str(message)+'\n')
            f.close()