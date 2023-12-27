from django.core.management.base import BaseCommand
import os
import subprocess

class Command(BaseCommand):
    help = 'Generate models, serializers and simple CRUD'
    
    def generate_models(self,new_directory):
        list_properties =[]
        modal_name = input('Class name of the modal to create:\n> ')
        class_name = modal_name.capitalize()
        model_class_str = f'from django.db import models \n\nclass {class_name}(models.Model):\n'
        while True:
            property_name = input('New property name (press Enter to stop adding fields):\n> ')
            if not property_name:
                break
            while True:
                field_type = input('Field type (enter ? to see all types) [CharField]:\n> ')
                if field_type == "?":
                    print('- CharField\n- BooleanField\n- IntegerField\n- DateTimeField\n- relation')
                elif field_type in ['CharField', 'BooleanField', 'IntegerField', 'DateTimeField', 'relation']:
                    break
                else:
                    print('Invalid field type. Please enter a valid field type or "?" to see all types.')
            if field_type =="CharField":
                list_properties.append([property_name,field_type])
                model_class_str += f'    {property_name} = models.CharField('
                max_length = input('Field length [200]:\n> ')
                if max_length=='':
                    max_length=200
                model_class_str += f'max_length={max_length}, '
                while True:    
                    null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                    if null =='yes':
                        model_class_str += f'null=True, '
                        break
                    elif null =='no':
                        model_class_str += f'null=False, '
                        break
                    else:
                        choice = print("Must be yes or no")
                while True:
                    unique = input('Can this field be unique in the database (yes/no)\n> ')
                    if unique =='yes':
                        model_class_str += f'unique=True)\n'
                        break
                    elif unique =='no':
                        model_class_str += f'unique=False)\n'
                        break
                    else:
                        choice = print("Must be yes or no")
            if field_type =="BooleanField":
                list_properties.append([property_name,field_type])
                model_class_str += f'    {property_name} = models.BooleanField('
                while True:
                    null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                    if null =='yes':
                        model_class_str += f'null=True, '
                        break
                    elif null =='no':
                        model_class_str += f'null=False, '
                        break
                    else:
                        choice = print("Must be yes or no")
                while True:
                    default = input('Can this field be default in the database (true/false)\n> ')
                    if default =='true':
                        model_class_str += f'default=True)\n'
                        break
                    elif default =='false':
                        model_class_str += f'default=False)\n'
                        break
                    else:
                        choice = print("Must be true or false")
            if field_type =="IntegerField":
                list_properties.append([property_name,field_type])
                model_class_str += f'    {property_name} = models.IntegerField('
                while True:
                    null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                    if null =='yes':
                        model_class_str += f'null=True, '
                        break
                    elif null =='no':
                        model_class_str += f'null=False, '
                        break
                    else:
                        choice = print("Must be yes or no")
                while True:
                    unique = input('Can this field be unique in the database (yes/no)\n> ')
                    if unique =='yes':
                        model_class_str += f'unique=True)\n'
                        break
                    elif unique =='no':
                        model_class_str += f'unique=False)\n'
                        break
                    else:
                        choice = print("Must be yes or no")
                while True:
                    default = input('Can this field be default in the database (true/false)\n> ')
                    if default !='':
                        default_value  = input('entre your default value:\n> ')
                        model_class_str += f'default={default_value})\n'
                        break
                    else:
                        break
            if field_type =="DateTimeField":
                list_properties.append([property_name,field_type])
                model_class_str += f'    {property_name} = models.DateTimeField('
                while True:
                    null = input('Can this field be null in the database (nullable) (yes/no)\n> ')
                    if null =='yes':
                        model_class_str += f'null=True, '
                        break
                    elif null =='no':
                        model_class_str += f'null=False, '
                        break
                    else:
                        choice = print("Must be yes or no")
            if field_type =="relation":
                while True:
                    class_relation = input('What class should this entity be related to?:\n> ')
                    result = subprocess.run(['python', 'manage.py', 'find_model', class_relation],
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if 'Found the model class' in result.stdout:
                        lines = result.stdout.split('\n')
                        model_class_line = next((line for line in lines if 'Found the model class' in line), None)
                        
                        if model_class_line:
                            # Extract the app name using string manipulation or regex
                            app_name_start = model_class_line.find("in app '") + len("in app '")
                            app_name_end = model_class_line.find("'", app_name_start)
                            app_name = model_class_line[app_name_start:app_name_end]
                            print(f"Found the model class '{class_relation}' in app '{app_name}'.")
                            if app_name in new_directory:
                                pass
                            else:
                                formatted_model_class_str = f'from {app_name}.models import {class_relation}\n'+model_class_str
                                model_class_str=formatted_model_class_str
                            type_relation = input('Relation type? [ManyToOne, ManyToMany]:\n> ')
                            while True:
                                if type_relation == 'ManyToOne':
                                    list_properties.append([class_relation,property_name,field_type,'ManyToOne',app_name])
                                    model_class_str += f'    {property_name} = models.ForeignKey({class_relation}, on_delete=models.CASCADE)'
                                    break
                                elif type_relation == 'ManyToMany':
                                    list_properties.append([class_relation,property_name,field_type,'ManyToMany',app_name])
                                    model_class_str += f'    {property_name} = models.ManyToManyField({class_relation})'
                                    break
                                else:
                                    print('Invalid relation type. Please enter a valid field type.')
                            break
                        else:
                            print("Model class line not found in the output.")
                            break
                    else:
                        print("Model class not found.")
                        break

        model_class_str += '\n    class Meta:\n        db_table = \'' + modal_name.lower() + '\'\n\n'
        with open(f"{new_directory}/models.py", "w") as model_file:
            model_file.write(model_class_str) 
        return modal_name,list_properties 
    
    def generate_serializer(self,new_directory,modal_name,lista):
        class_name = modal_name.capitalize()+'Serializer'
        fields = lista
        related_fields=[]
        code = f"""from rest_framework import serializers
from .models import {modal_name.capitalize()}

class {class_name}(serializers.ModelSerializer):
    """
        for index, sublist in enumerate(lista):
            # Check if "relation" is present in the sublist
            if 'relation' in sublist:
                formated_code = f'from {sublist[4]}.models import {sublist[0]}\n'+code
                code = formated_code
                if 'ManyToMany' in sublist:
                    related_fields.append({"field_name": sublist[1], "type": "serializers.PrimaryKeyRelatedField", "many": True, "queryset": sublist[0]+".objects.all()"})
                else:
                    related_fields.append({"field_name": sublist[1], "type": "serializers.PrimaryKeyRelatedField", "queryset": sublist[0]+".objects.all()"})
                    
        for field in related_fields:
            field_name = field["field_name"]
            field_type = field["type"]
            code += f"    {field_name} = {field_type}({', '.join([f'{key}={value}' for key, value in field.items() if key not in ['field_name', 'type']])})"
            code += "\n"

        code += f"""
    class Meta:
        model = {modal_name.capitalize()}
        fields = '__all__'
            
    """
        with open(f"{new_directory}/serializer.py", "w") as model_file:
            model_file.write(code)
            
    def generate_crud(self,new_directory,app_name,modal_name):
        class_name = modal_name.capitalize()
        code = f"""from django.core import serializers
import json
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .models import {class_name}

"""
        code+=f"""
def {class_name}All(request):
    {modal_name} = {class_name}.objects.all()
    {modal_name}_dict = serializers.serialize("json", {modal_name})
    res = json.loads({modal_name}_dict)
    return JsonResponse({{"resultat": res}})\n\n
"""

        code+=f"""
def {class_name}Detail(request,id):
    {modal_name} = {class_name}.objects.filter(id=id)
    {modal_name}_dict = serializers.serialize("json", {modal_name})
    res = json.loads({modal_name}_dict)
    return JsonResponse({{"resultat": res}})\n\n
"""
        
        formated_code = f'from .serializer import *\n'+code
        code = formated_code
        code+=f"""
def {class_name}Create(request):
    data = JSONParser().parse(request)
    serializer  = {class_name}Serializer(data=data)
    if serializer.is_valid():
        serializer.save()
    return JsonResponse({{"message": "added successfully"}})\n\n
"""
        
        code+=f"""
def {class_name}Delete(request,id):
    {modal_name} = {class_name}.objects.get(id=id)
    {modal_name}.delete()
    return JsonResponse({{"message": "deleted successfully"}})\n\n
"""
        
        code+=f"""
def {class_name}Update(request,id):
    data = JSONParser().parse(request)
    {modal_name} = {class_name}.objects.get(id=id)
    serializer = {class_name}Serializer({modal_name},data=data)
    if serializer.is_valid():
        serializer.save()
    return JsonResponse({{"message": "updated successfully"}})\n\n
"""

        with open(f"{new_directory}/views.py", "w") as model_file:
            model_file.write(code)
        
    def generate_url(self,new_directory,app_name,modal_name,bool,your_settingFile_directory):
        code=f"""from django.urls import path, include
from . import views
"""
        urlpatterns = []
        urlpatterns_content = f"""
        path('{modal_name.capitalize()}All', views.{modal_name.capitalize()}All, name='{modal_name.capitalize()}All'),
        path('{modal_name.capitalize()}Detail/<int:id>', views.{modal_name.capitalize()}Detail, name='{modal_name.capitalize()}Detail'),
        path('{modal_name.capitalize()}Create', views.{modal_name.capitalize()}Create, name='{modal_name.capitalize()}Create'),
        path('{modal_name.capitalize()}Delete/<int:id>', views.{modal_name.capitalize()}Delete, name='{modal_name.capitalize()}Delete'),
        path('{modal_name.capitalize()}Update/<int:id>', views.{modal_name.capitalize()}Update, name='{modal_name.capitalize()}Update'),
        """
        urlpatterns.append(urlpatterns_content)
        urlpatterns_string = 'urlpatterns = ['+''.join(urlpatterns)
        code+=urlpatterns_string+']'
        
        with open(your_settingFile_directory+'/urls.py', "r") as f:
            content = f.read()

        # Find the INSTALLED_APPS list in the content
        start_index = content.find("urlpatterns  = [") + len("urlpatterns  = [")
        end_index = content.find("]", start_index)

        # Extract the INSTALLED_APPS list
        installed_apps = content[start_index:end_index].strip()
        if bool==True:
            # Add the new app to the list
            path = f"path('backend.{app_name}/', include('backend.{app_name}.urls'))"
            updated_installed_apps = installed_apps[:-1] + installed_apps[-1] + f'\n    {path},\n' 
        else:
            path = f"path('{app_name}/', include('{app_name}.urls'))"
            # Add the new app to the list
            updated_installed_apps = installed_apps[:-1] + installed_apps[-1] + f'\n    {path},\n' 

        # Replace the old INSTALLED_APPS list with the updated one
        updated_content = content[:start_index] + updated_installed_apps + content[end_index:]

        with open(your_settingFile_directory+'/urls.py', "w") as f:
            f.write(updated_content)
        with open(f"{new_directory}/urls.py", "w") as model_file:
            model_file.write(code)
            
    def find_folder(self,start_path, folder_name):
        for root, dirs, files in os.walk(start_path):
            if folder_name in dirs:
                return os.path.join(root, folder_name)

        return None
    
    def find_manage_directory(self,start_dir, file_name):
        for root, dirs, files in os.walk(start_dir):
            if file_name in files:
                return os.path.abspath(root)

        return None
    
    def handle(self, *args, **options):
        app_name = input("Your app name?: ")
        folder_path = self.find_folder('/', app_name)
        modal_name,list_properties=self.generate_models(folder_path)
        while True:
            create_serializer = input('do you want to create serializer?: ')
            if create_serializer == "yes":
                self.generate_serializer(folder_path,modal_name,list_properties)
                while True:
                    create_crud = input('do you want to create simple CRUD?: ')
                    if create_crud == "yes":
                        self.generate_crud(folder_path,app_name,modal_name)
                        folder_path = self.find_folder('/', app_name)
                        # Split the path using the directory separator '/'
                        path_elements = folder_path.split(os.path.sep)
                        new_path_elements = path_elements[:-1]
                        new_path = os.path.sep.join(new_path_elements)
                        manage_path = self.find_manage_directory(new_path, 'manage.py')
                        settings_path = self.find_manage_directory(new_path, 'settings.py')
                        if settings_path ==None:
                            new_path_elements = path_elements[:-2]
                            new_path = os.path.sep.join(new_path_elements)
                            manage_path = self.find_manage_directory(new_path, 'manage.py')
                            settings_path = self.find_manage_directory(new_path, 'settings.py')
                        if folder_path != manage_path+'/'+app_name:
                            self.generate_url(folder_path,app_name,modal_name,True,settings_path)
                        else:
                            self.generate_url(folder_path,app_name,modal_name,False,settings_path)
                        break
                    elif create_crud == "no":
                        break
                    else:
                        choice = input("Must be yes or no.\n")
                break
            elif create_serializer == "no":
                break
            else:
                choice = input("Must be yes or no.\n")