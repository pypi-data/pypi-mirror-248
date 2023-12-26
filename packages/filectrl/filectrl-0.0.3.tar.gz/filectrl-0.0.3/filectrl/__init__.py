import os
import enum
import inspect

class WriteType(enum.Enum):
    Text = 0
    Data = 1

__caller_code_key = '1.^.self.caller_path'

class FileController:
    def __init__(self, write_type:WriteType, **kwargs) -> None:
        self.data_separator = ','
        self.file_name = ''
        self.file_type = 'log'
        self.logging_path = '.'
        self.backup_path = 'logs'
        
        self.__write_type = write_type
        self.__excuted_path = ''
        self.__caller_path = ''
        
        if __caller_code_key in kwargs:
            self.__caller_path = kwargs[__caller_code_key]
            caller_path_split = self.__caller_path.split('/')
            self.file_name = caller_path_split[-2]
            self.__excuted_path = '/'.join(caller_path_split[:-1])
            
        if 'data_separator' in kwargs:
            self.data_separator = kwargs['data_separator']
        
        if 'file_name' in kwargs:
            self.file_name = kwargs['file_name']
        
        if 'file_type' in kwargs:
            self.file_type = kwargs['file_type']
        
        if 'logging_path' in kwargs:
            self.__excuted_path = self.__convert_absolute_path(self.__caller_path, kwargs['logging_path'])
            self.logging_path = self.__excuted_path
        else:
            self.logging_path = self.__convert_absolute_path(self.__caller_path, self.logging_path)
        
        if 'backup_path' in kwargs:
            self.backup_path = self.__convert_absolute_path(self.__caller_path, kwargs['backup_path'])
        else:
            self.backup_path = self.__convert_absolute_path(self.__caller_path, self.backup_path)
        
         
    def write(self, *args, **kwargs):
        match self.__write_type:
            case WriteType.Text:
                self.__write_text(*args, **kwargs)
                
            case WriteType.Data:
                self.__write_data(*args, **kwargs)
                
            case _:
                pass
                
    def __write_text(self, *args, **kwargs):
        str_list = []
        for arg in args:
            str_list.append(str(arg))
        joins = ' '.join(str_list)
    
        with open(f"{self.logging_path}/{self.file_name}.{self.file_type}", 'a') as f:
            f.write(f"{joins}\n")
        
    def __write_data(self, *args, **kwargs):
        data_list = []
        for arg in args:
            data_list.append(str(arg))
        for key, val in kwargs.items():
            data_list.append(f"{{{key} : {val}}}")
        
        joins = self.data_separator.join(data_list)
        with open(f"{self.logging_path}/{self.file_name}.{self.file_type}", 'a') as f:
            f.write(f"{joins}\n")
        
    def __convert_absolute_path(self, caller_file_path:str, src_path:str) -> str:
        dst_path = src_path
        if dst_path == '':
            dst_path = '.'
            
        spiltted_dst_path = dst_path.split('/')
        
        if spiltted_dst_path[0] == '~':
            dst_path = os.path.expanduser(dst_path)
            
        elif spiltted_dst_path[0] == '..':
            splited_frame_path = caller_file_path.split('/')
            joined_frame_path = '/'.join(splited_frame_path[:-2])
            dst_path = joined_frame_path + (dst_path[2:] if 2<len(dst_path) else "")
            
        elif spiltted_dst_path[0] == '.':
            splited_frame_path = caller_file_path.split('/')
            joined_frame_path = '/'.join(splited_frame_path[:-1])
            dst_path = joined_frame_path + (dst_path[1:] if 1<len(dst_path) else "")
        
        else:
            splited_frame_path = caller_file_path.split('/')
            joined_frame_path = '/'.join(splited_frame_path[:-1])
            dst_path = joined_frame_path + '/' + src_path
            
        return dst_path
        
def get_controller(write_type:WriteType=WriteType.Text, **kwargs):
    '''
    Parameters
    -
    write_type (filectrl.WriteType): Text, Data (default: .Text)\n
    data_separator (str): write_type == filectrl.WriteType.Data (default: ',')\n
    file_name (str): log file name. (default: ''; project directory name)\n
    file_type (str): log file extension name. (default: 'log')\n
    logging_path (str): logging path (default: '.')\n
    backup_path (str): Backup path for logged file. (default: './logs')\n

    '''
    stacks = inspect.stack()
    kwargs[__caller_code_key] = stacks[1].filename
    return FileController(write_type, **kwargs)