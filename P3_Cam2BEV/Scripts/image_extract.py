import matplotlib.pyplot as plt
import matplotlib.image as img
import pathlib
from nuscenes.nuscenes import NuScenes
import os 
import shutil
import yaml
from Scripts.utils import quart_to_angles
from Scripts.ipm import generate_ipm_image
import streamlit as st
from PIL import Image
import pathlib as path
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
        # fig = plt.figure(figsize=(30, 10))
        # rows = 1
        # columns =10
        count =0 
        cols = st.columns(4)
        for i in pathlib.Path(input_path).iterdir():
            if not (i.is_file()):
                count+=1
                path = str(i/img_name)
                im = img.imread(path)
                count=count%4
                cols[count].image(im,i.parts[-1],width = 200,use_column_width=True)
                # fig.add_subplot(rows, columns, count)
                # plt.imshow(im)
                # plt.axis('off')
                # plt.title(i.parts[-1])

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

        rotation_dict = {}
        rotation_dict["CAM_FRONT"]={"yaw":0,"pitch":0,"roll":0}
        rotation_dict["CAM_BACK"]={"yaw":180,"pitch":0,"roll":0}
        rotation_dict["CAM_FRONT_LEFT"]={"yaw":60,"pitch":0,"roll":0}
        rotation_dict["CAM_FRONT_RIGHT"]={"yaw":-60,"pitch":0,"roll":0}
        rotation_dict["CAM_BACK_RIGHT"]={"yaw":-120,"pitch":0,"roll":0}
        rotation_dict["CAM_BACK_LEFT"]={"yaw":120,"pitch":0,"roll":0}

        self.rotation_dict = rotation_dict
        return 

    def create_folder(self,n):
        path = self.parent+self.dir+"\\"+str(n)

        if not os.path.exists(self.parent+self.dir):
             os.mkdir(self.parent+self.dir)

        if not os.path.exists(path):
            os.mkdir(path)
            os.mkdir(path+"\images")
            os.mkdir(path+"\config_logs")
            os.mkdir(path+"\config")
        else:
            print("path already exists ,  Change the output folder name")
        return 


    def generate_1_bev(self,sample,n):
        ##Generate folder structure for input
        # print("processing sample",sample)
        self.create_folder(n)

        ## create input config and image files for IPM ops
        camera_img_pair = []
        for angle in self.image_angles:
            json_info =  self.nuscene_data_obj.get('sample_data', sample['data'][angle])
            file_name =json_info["filename"]
            ego_pose =self.nuscene_data_obj.get("ego_pose", json_info["ego_pose_token"])
            calibrated_sensor_data = self.nuscene_data_obj.get("calibrated_sensor",json_info["calibrated_sensor_token"])
            # store the image in the input file path
            image_path  = self.parent+self.dir+"\\"+str(n)+"\images"+'\\'+angle+".jpg"
            shutil.copyfile( self.dataroot_nuscene+file_name,image_path )
            ## Create config logs 
            config_file_logs = self.parent+self.dir+"\\"+str(n)+"\config_logs\\"+angle+'.yaml'
            with open(config_file_logs,'w') as cf:
                yaml.dump({"sensor data":calibrated_sensor_data}  , cf, default_flow_style=False)
                yaml.dump({"egopose":ego_pose}  , cf, default_flow_style=False)
            cf.close()

            ## Create configs file from logs 
            config_file = self.parent+self.dir+"\\"+str(n)+"\config\\"+angle+'.yaml'
            cam2bev_config = self.create_cam2bev_config(self.parent+self.dir,calibrated_sensor_data,ego_pose,angle)
            with open(config_file,'w') as cf:
                yaml.dump(  cam2bev_config, cf, default_flow_style=False)
                cf.close()
            camera_img_pair.append(config_file)
            camera_img_pair.append(image_path)


        ## Drone files to be copied as is from master
        drone_file_loc = r"C:\Users\IHG6KOR\Desktop\shiv\Portfolio\shivensingh2013.github.io\P3_Cam2BEV\Scripts\drone.yaml"
        shutil.copyfile( drone_file_loc, self.parent+self.dir+"\\"+str(n)+"\config\drone.yaml")
        # create_output_folder()
        # Run IPM
        args = {}
        args["output"]= self.create_output_folder()
        args["batch"] = False
        args["camera_img_pair"] = camera_img_pair
        args["drone"] = self.parent+self.dir+"\\"+str(n)+"\config\drone.yaml"
        args["r"] = 20
        args["wm"] = 20
        args["hm"] =40
        args["v"] = False
        args["cc"] = False
        args["outfile_name"] = str(n) + ".jpg"

        generate_ipm_image(args)

        return

    ## generate BEV images for all the scenes provided inside the datapath folder
    # Input - datapath :  Path of the folder containing folders 1 to n with each subfolder conatining nuscenes images along with config
    def generate_BEV_from_images(self):
        in_path = path.Path(self.parent+self.dir)

        ## input image and config folder already present
        output_loc =self.create_output_folder()

        for fld in in_path.iterdir():
            sample_num = str(fld.parts[-1])
            camera_img_pair = []
            st.write("Reading folder number" , fld.parts[-1])

            for image in path.Path(fld/"images").iterdir():
                camera_img_pair.append(str(path.Path(fld/"config"/(image.parts[-1].split(".")[0]+".yaml"))))
                camera_img_pair.append(str(image))
            print(camera_img_pair)
            # st.write(camera_img_pair)
            # Run IPM
            args = {}
            args["output"]= output_loc
            args["batch"] = False
            args["camera_img_pair"] = camera_img_pair
            args["drone"] = self.parent+self.dir+"\\"+str(sample_num)+"\config\drone.yaml"
            args["r"] = 20
            args["wm"] = 20
            args["hm"] =40
            args["v"] = False
            args["cc"] = False
            args["outfile_name"] = str(sample_num) + ".jpg"

            generate_ipm_image(args)


    def generate_n_BEV(self):
        next_token = self.scene_obj['first_sample_token']
        count= 0
        while(1>0):
            count+=1
            if next_token  == self.scene_obj['last_sample_token'] or count > 10:
                break
            else: 
                my_sample =  self.nuscene_data_obj.get('sample',next_token)   
                self.generate_1_bev(my_sample,count)
                next_token = my_sample["next"]
                # print("Now processing", next_token)
            st.text(str(count) +" / 10 sample processed")
        return 

    def create_cam2bev_config(self, path, sensor, egopose,angle):

        result = {}

        result['fx'] = sensor["camera_intrinsic"][0][0]
        result['fy'] = sensor["camera_intrinsic"][1][1]

        result['px'] = sensor["camera_intrinsic"][0][2]
        result['py'] = sensor["camera_intrinsic"][1][2]

        ## rotation 
        # result["yaw"],result["pitch"],result["roll"] =   quart_to_angles(sensor['rotation'])

        ## TODO - make yaw,pithc and roll as standard - rule based
        res = self.rotation_dict[angle]
        result["yaw"],result["pitch"],result["roll"] = res["yaw"],res["pitch"],res["roll"]

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

        return outpath


    def print_result(self,inp,out,folder,frame):
        ## print inputs to streamlit and outputs to streamlit as an animation frame level
        st.text("Input camera images")
        count =0 
        col_count = 3
        cols = st.columns(col_count)
        for i in pathlib.Path(inp+folder+"//"+str(frame)+"/images").iterdir():
            count+=1
            im = Image.open(i)
            count=count%col_count
            cols[count].image(im,i.parts[-1],width = 200,use_column_width=True)

        st.text("Output camera images")
        im = Image.open(out+folder+"//"+str(frame)+".jpg")
        st.image(im,"BEV",width = 400)
        return 





        
