import matplotlib.pyplot as plt
import matplotlib.image as img
import pathlib
from nuscenes.nuscenes import NuScenes
import os 
import shutil
import yaml

class cam2bev_image:
    
    def __init__(self,image_name:str, input_path:str):
        super().__init__()
        self.image_name = image_name
        self.input_path = input_path
        return
    
    def get_image(self):
        return

    def print_image(self,input_path:str,img_name:str):
        # create figure
        fig = plt.figure(figsize=(30, 10))
        rows = 1
        columns =7
        count =0 
        for i in pathlib.Path(input_path).iterdir():
            if not (i.is_file()):
                count+=1
                fig.add_subplot(rows, columns, count)
                path = str(i/img_name)
                im = img.imread(path)
                plt.imshow(im)
                plt.axis('off')
                plt.title(i.parts[-1])
        return



class nuscene_image:
    def __init__(self,scene,dataroot_nuscene,dir,parent,out_parent):
        super().__init__()
        self.image_angles =  ["CAM_FRONT","CAM_BACK","CAM_FRONT_LEFT","CAM_FRONT_RIGHT","CAM_BACK_RIGHT","CAM_BACK_LEFT"]
        self.scene = scene
        self.dataroot_nuscene  = dataroot_nuscene
        self.dir = dir
        self.parent = parent
        self.nuscene_data_obj = NuScenes(version='v1.0-mini', dataroot=self.dataroot_nuscene, verbose=False)
        self.scene_obj = self.nuscene_data_obj.scene[self.scene]
        self.first_sample_token = self.scene_obj['first_sample_token']
        self.out_parent = out_parent
        return 

    def create_folder(self):
        path = self.parent+self.dir
        if not os.path.exists(path):
            os.mkdir(path)
            os.mkdir(path+"\images")
            os.mkdir(path+"\config_logs")
            os.mkdir(path+"\config")
            print("Created folders")
        else:
            print("path already exists ,  Change the output folder name")
        return 

    # def get_sample(self,sample_token):
    #     self.sample_token = sample_token
    #     my_sample = self.nuscene_data_obj.get('sample', sample_token)
    #     return my_sample



    def generate_1_bev(self,sample):
        for angle in self.image_angles:
            json_info =  self.nuscene_data_obj.get('sample_data', sample['data'][angle])
            file_name =json_info["filename"]
            ego_pose =self.nuscene_data_ob.get("ego_pose", json_info["ego_pose_token"])
            calibrated_sensor_data = self.nuscene_data_ob.get("calibrated_sensor",json_info["calibrated_sensor_token"])
            # store the image in the input file path
            shutil.copyfile( self.dataroot_nuscene+file_name, self.parent+self.dir+"\images"+'\\'+angle+".jpg")

            
        ## Create config logs 
            config_file_logs = self.parent+self.dir+"\config_logs\\"+angle+'.yaml'
            
            with open(config_file_logs,'w') as cf:
                yaml.dump({"sensor data":calibrated_sensor_data}  , cf, default_flow_style=False)
                yaml.dump({"egopose":ego_pose}  , cf, default_flow_style=False)
            cf.close()

        ## Create configs file from logs 
            config_file = self.parent+self.dir+"\config\\"+angle+'.yaml'
            cam2bev_config = create_cam2bev_config(self.parent+self.dir,calibrated_sensor_data,ego_pose )

            with open(config_file,'w') as cf:
                yaml.dump(  cam2bev_config, cf, default_flow_style=False)

            # yaml.dump( , cf, default_flow_style=False)
        ## Create 1 drone yaml file from logs 

        # drone = path+"\config\drone.yaml'
        # with open(drone,'w') as cf:

            # yaml.dump( , cf, default_flow_style=False)
        # cf.close()
            # print(file_name)
        print(len(self.image_angles) , "IMAGES LOADED TO INPUT FOLDER")
        create_output_folder()

        ## TODO - Need to run the ipm code with the right parameters
        run_ipm()
        return

    def generate_n_BEV(self):
        next_token = self.scene_obj['first_sample_token']
        while():
            if next_token  == self.scene_obj['last_sample_token']:
                break
            else: 
                my_sample =  self.nuscene_data_obj.get('sample',next_token)   
                generate_1_bev(my_sample)
                next_token = my_sample["next"]
        print("Generation of results complete")
        return 

    def create_cam2bev_config(self, path, sensor, egopose):
        result ={}

        result['fx'] = sensor["camera_intrinsic"][0][0]
        result['fy'] = sensor["camera_intrinsic"][1][1]

        result['px'] = sensor["camera_intrinsic"][0][2]
        result['py'] = sensor["camera_intrinsic"][1][2]

        ## rotation 
        # result["yaw"],result["pitch"],result["roll"] =   quart_to_angles(sensor['rotation'])

        ## TODO - make yaw,pithc and roll as standard - rule based


        ## translation
        result["XCam"] =sensor["translation"][0]
        result["YCam"] = sensor["translation"][1]
        result["ZCam"] =sensor["translation"][2]

        return result
    
    def create_output_folder(self):
        outpath = self.out_parent+self.dir
        if not os.path.exists(outpath):
            os.mkdir(outpath)
            print("Created folders at",outpath)
        else:
            print("path already exists ,  check name of path")

        return

    





        
