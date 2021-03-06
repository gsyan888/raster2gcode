'''
# ----------------------------------------------------------------------------
# Copyright (C) 2014 305engineering <305engineering@gmail.com>
# Original concept by 305engineering.
#
# "THE MODIFIED BEER-WARE LICENSE" (Revision: my own :P):
# <305engineering@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff (except sell). If we meet some day, 
# and you think this stuff is worth it, you can buy me a beer in return.
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ----------------------------------------------------------------------------
'''


import sys
import os
import re

sys.path.append('/usr/share/inkscape/extensions')
sys.path.append('/Applications/Inkscape.app/Contents/Resources/extensions') 

import subprocess
import math

import inkex
import png
import array


class GcodeExport(inkex.Effect):

########     Richiamata da _main()
    def __init__(self):
        """init the effetc library and get options from gui"""
        inkex.Effect.__init__(self)
        
        #use arg_parser attribute to check inkex version
        #add arguments/options
        if hasattr(self, "arg_parser") :
            #
            # for Inkscape 1.x
            #
            
            #add by gsyan
            self.arg_parser.add_argument("--active-tab", default="options", help="Defines which tab is active")

            # Opzioni di esportazione dell'immagine
            self.arg_parser.add_argument("-d", "--directory",action="store", dest="directory", default="/home/",help="Directory for files") ####check_dir
            self.arg_parser.add_argument("-f", "--filename", action="store", dest="filename", default="-1.0", help="File name")            
            self.arg_parser.add_argument("--add-numeric-suffix-to-filename", action="store", type=inkex.Boolean, dest="add_numeric_suffix_to_filename", default=True,help="Add numeric suffix to filename")            
            self.arg_parser.add_argument("--bg_color",action="store",type=str,dest="bg_color",default="",help="")
            self.arg_parser.add_argument("--resolution",action="store", type=int, dest="resolution", default="5",help="") #Usare il valore su float(xy)/resolution e un case per i DPI dell export
            
            
            # Come convertire in scala di grigi
            self.arg_parser.add_argument("--grayscale_type",action="store", type=int, dest="grayscale_type", default="1",help="") 
            
            # Modalita di conversione in Bianco e Nero 
            self.arg_parser.add_argument("--conversion_type",action="store", type=int, dest="conversion_type", default="1",help="") 
            
            # Opzioni modalita 
            self.arg_parser.add_argument("--BW_threshold",action="store", type=int, dest="BW_threshold", default="128",help="grayscale enable variable speed") 
            self.arg_parser.add_argument("--grayscale_resolution",action="store", type=int, dest="grayscale_resolution", default="1",help="the max speed for grayscale when enable variable speed") 
            
            #Velocita Nero e spostamento
            self.arg_parser.add_argument("--speed_OFF",action="store", type=int, dest="speed_OFF", default="1200",help="") 
            self.arg_parser.add_argument("--speed_ON",action="store", type=int, dest="speed_ON", default="200",help="") 
            
            #Options for greayscale to variable speed : add by gsyan
            self.arg_parser.add_argument("--var_speed_on",action="store", type=inkex.Boolean, dest="var_speed_on", default=False,help="")
            self.arg_parser.add_argument("--var_speed_on_max",action="store", type=int, dest="var_speed_on_max", default="2000",help="") 

            # Mirror Y
            self.arg_parser.add_argument("--flip_y",action="store", type=inkex.Boolean, dest="flip_y", default=False,help="")
            
            # Homing
            self.arg_parser.add_argument("--homing",action="store", type=int, dest="homing", default="1",help="")

            # Commands
            self.arg_parser.add_argument("--laseron", action="store", dest="laseron", default="M106 S255", help="laser power on command : M03, M106 Sxxx, M42 Px Sxxx")
            self.arg_parser.add_argument("--laseroff", action="store", dest="laseroff", default="M107", help="laser power off command : M05, M107, M42 Px S0")

            self.arg_parser.add_argument("--laseron_delay", action="store", type=int, dest="laseron_delay", default="0", help="")
            self.arg_parser.add_argument("--laser_mini_power", action="store", type=int, dest="laser_mini_power", default="0", help="")
            self.arg_parser.add_argument("--laser_max_power", action="store", type=int, dest="laser_max_power", default="255", help="")
            
            
            # Anteprima = Solo immagine BN 
            self.arg_parser.add_argument("--preview_only",action="store", type=inkex.Boolean, dest="preview_only", default=False,help="") 
        else :
            #
            # for Inkscape 0.92
            #
            
            #add by gsyan
            self.OptionParser.add_option("--active-tab", default="options", help="Defines which tab is active")

            # Opzioni di esportazione dell'immagine
            self.OptionParser.add_option("-d", "--directory",action="store", type="string", dest="directory", default="/home/",help="Directory for files") ####check_dir
            self.OptionParser.add_option("-f", "--filename", action="store", type="string", dest="filename", default="-1.0", help="File name")            
            self.OptionParser.add_option("","--add-numeric-suffix-to-filename", action="store", type="inkbool", dest="add_numeric_suffix_to_filename", default=True,help="Add numeric suffix to filename")            
            self.OptionParser.add_option("","--bg_color",action="store",type="string",dest="bg_color",default="",help="")
            self.OptionParser.add_option("","--resolution",action="store", type="int", dest="resolution", default="5",help="") #Usare il valore su float(xy)/resolution e un case per i DPI dell export
            
            
            # Come convertire in scala di grigi
            self.OptionParser.add_option("","--grayscale_type",action="store", type="int", dest="grayscale_type", default="1",help="") 
            
            # Modalita di conversione in Bianco e Nero 
            self.OptionParser.add_option("","--conversion_type",action="store", type="int", dest="conversion_type", default="1",help="") 
            
            # Opzioni modalita 
            self.OptionParser.add_option("","--BW_threshold",action="store", type="int", dest="BW_threshold", default="128",help="grayscale enable variable speed") 
            self.OptionParser.add_option("","--grayscale_resolution",action="store", type="int", dest="grayscale_resolution", default="1",help="the max speed for grayscale when enable variable speed") 
            
            #Velocita Nero e spostamento
            self.OptionParser.add_option("","--speed_OFF",action="store", type="int", dest="speed_OFF", default="1200",help="") 
            self.OptionParser.add_option("","--speed_ON",action="store", type="int", dest="speed_ON", default="200",help="") 
            
            #Options for greayscale to variable speed : add by gsyan
            self.OptionParser.add_option("","--var_speed_on",action="store", type="inkbool", dest="var_speed_on", default=False,help="")
            self.OptionParser.add_option("","--var_speed_on_max",action="store", type="int", dest="var_speed_on_max", default="2000",help="") 

            # Mirror Y
            self.OptionParser.add_option("","--flip_y",action="store", type="inkbool", dest="flip_y", default=False,help="")
            
            # Homing
            self.OptionParser.add_option("","--homing",action="store", type="int", dest="homing", default="1",help="")

            # Commands
            self.OptionParser.add_option("","--laseron", action="store", type="string", dest="laseron", default="M03", help="laser power on command : M03, M106 Sxxx, M42 Px Sxxx")
            self.OptionParser.add_option("","--laseroff", action="store", type="string", dest="laseroff", default="M05", help="laser power off command : M05, M107, M42 Px S0")

            self.OptionParser.add_option("","--laseron_delay", action="store", type="int", dest="laseron_delay", default="0", help="")
            self.OptionParser.add_option("","--laser_mini_power", action="store", type="int", dest="laser_mini_power", default="0", help="")
            self.OptionParser.add_option("","--laser_max_power", action="store", type="int", dest="laser_max_power", default="255", help="")
            
            
            # Anteprima = Solo immagine BN 
            self.OptionParser.add_option("","--preview_only",action="store", type="inkbool", dest="preview_only", default=False,help="") 
        
        #inkex.errormsg("BLA BLA BLA Messaggio da visualizzare") #DEBUG

        
########     Richiamata da __init__()
########    Qui si svolge tutto
    def effect(self):
        
        if hasattr(self, "arg_parser") :
            #
            # for Inkscape 1.x
            #
            current_file = self.options.input_file #modified by gsyan
        else :
            #
            # for Inkscape 0.92
            #
            current_file = self.args[-1]
        
        bg_color = self.options.bg_color
        
        
        ##Implementare check_dir
        
        if (os.path.isdir(self.options.directory)) == True:                    
            
            ##CODICE SE ESISTE LA DIRECTORY
            #inkex.errormsg("OK") #DEBUG
            
            
            #Aggiungo un suffisso al nomefile per non sovrascrivere dei file
            if self.options.add_numeric_suffix_to_filename :
                dir_list = os.listdir(self.options.directory) #List di tutti i file nella directory di lavoro
                #temp_name =  self.options.filename    #remark by gsyan
                #modified by gsyan : split filename to root name and extension
                temp_name,fileExtension = os.path.splitext(self.options.filename)
                
                max_n = 0
                for s in dir_list :
                    r = re.match(r"^%s_0*(\d+)%s$"%(re.escape(temp_name),'.png' ), s)
                    if r :
                        max_n = max(max_n,int(r.group(1)))    
                self.options.filename = temp_name + "_" + ( "0"*(4-len(str(max_n+1))) + str(max_n+1) )
                
            else : #add by gsyan
                self.options.filename,fileExtension = os.path.splitext(self.options.filename)
                

            #genero i percorsi file da usare
            
            suffix = ""
            if self.options.conversion_type == 1:
                suffix = "_BWfix_"+str(self.options.BW_threshold)+"_"
            elif self.options.conversion_type == 2:
                suffix = "_BWrnd_"
            elif self.options.conversion_type == 3:
                suffix = "_H_"
            elif self.options.conversion_type == 4:
                suffix = "_Hrow_"
            elif self.options.conversion_type == 5:
                suffix = "_Hcol_"
            elif self.options.conversion_type == 7:
                suffix = "_H_error_"
            elif self.options.conversion_type == 8:
                suffix = "_H_ordered_"
            elif self.options.conversion_type == 9:
                suffix = "_H_pattern_"
            else:
                if self.options.grayscale_resolution == 1:
                    suffix = "_Gray_256_"
                elif self.options.grayscale_resolution == 2:
                    suffix = "_Gray_128_"
                elif self.options.grayscale_resolution == 4:
                    suffix = "_Gray_64_"
                elif self.options.grayscale_resolution == 8:
                    suffix = "_Gray_32_"
                elif self.options.grayscale_resolution == 16:
                    suffix = "_Gray_16_"
                elif self.options.grayscale_resolution == 32:
                    suffix = "_Gray_8_"
                else:
                    suffix = "_Gray_"
                
            
            pos_file_png_exported = os.path.join(self.options.directory,self.options.filename+".png") 
            pos_file_png_BW = os.path.join(self.options.directory,self.options.filename+suffix+"preview.png") 
            #pos_file_gcode = os.path.join(self.options.directory,self.options.filename+suffix+"gcode.txt") 
            #modified by gsyan : split filename then join root name , suffix and extension
            if fileExtension != '' :
                pos_file_gcode = os.path.join(self.options.directory,self.options.filename+suffix[:-1]+fileExtension)
            else:
                pos_file_gcode = os.path.join(self.options.directory,self.options.filename+suffix+"gcode.txt")
            
            

            #Esporto l'immagine in PNG
            self.exportPage(pos_file_png_exported,current_file,bg_color)


            
            #DA FARE
            #Manipolo l'immagine PNG per generare il file Gcode
            self.PNGtoGcode(pos_file_png_exported,pos_file_png_BW,pos_file_gcode)
                        
            
        else:
            inkex.errormsg("Directory does not exist! Please specify existing directory!")
            

            
            
########    ESPORTA L IMMAGINE IN PNG        
########     Richiamata da effect()
        
    def exportPage(self,pos_file_png_exported,current_file,bg_color):        
        ######## CREAZIONE DEL FILE PNG ########
        #Crea l'immagine dentro la cartella indicata  da "pos_file_png_exported"
        # -d 127 = risoluzione 127DPI  =>  5 pixel/mm  1pixel = 0.2mm
        ###command="inkscape -C -e \"%s\" -b\"%s\" %s -d 127" % (pos_file_png_exported,bg_color,current_file) 

        if self.options.resolution == 1:
            DPI = 25.4
        elif self.options.resolution == 2:
            DPI = 50.8
        elif self.options.resolution == 5:
            DPI = 127
        elif self.options.resolution == 10:    
            DPI = 254
        else:
            DPI = 25.4*self.options.resolution

        if hasattr(self, "arg_parser") :
            #
            # for Inkscape 1.x
            #
            command="inkscape -C -o \"%s\" -b \"%s\" -y 1.0 %s -d %d" % (pos_file_png_exported,bg_color,current_file,DPI) #Comando da linea di comando per esportare in PNG                    
            with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p :
                return_code = p.wait()
                f = p.stdout
                err = p.stderr
        else :
            #
            # for Inkscape 0.92
            #
            command="inkscape -C -e \"%s\" -b\"%s\" %s -d %s" % (pos_file_png_exported,bg_color,current_file,DPI) #Comando da linea di comando per esportare in PNG
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return_code = p.wait()
            f = p.stdout
            err = p.stderr


########    CREA IMMAGINE IN B/N E POI GENERA GCODE
########     Richiamata da effect()

    # by gsyan 
    def getLaserPowerValue(self,oldValue) :
        #return ( self.options.laser_mini_power + (255 - self.options.laser_mini_power)*oldValue/255 )
        return ( self.options.laser_mini_power + (self.options.laser_max_power - self.options.laser_mini_power)*oldValue/255 )
    
    # by gsyan 
    def getPixelValidValue(self,oldValue) :
        if oldValue < 0 :
            oldValue = 0
        if oldValue > 255 :
            oldValue = 255
        return oldValue
    
    #
    #intensity code from :
    #   https://github.com/abhishek-sehgal954/Inkscape_extensions_for_halftone_filters/blob/master/Raster_to_Raster/ordered_dithering.py
    #
    def intensity(self, arr):
        #  calcluates intensity of a pixel from 0 to 9
        mini = 999
        maxi = 0
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                maxi = max(arr[i][j],maxi)
                mini = min(arr[i][j],mini)
        level = float(float(maxi-mini)/float(10));
        brr = [[0]*len(arr[0]) for i in range(len(arr))]
        for i in range(10):
            l1 = mini+level*i
            l2 = l1+level
            if i==0 :		#first level set l1 to mini, modified by gsyan
                l1 = mini
            if i==9 :		#last lvel set l2 to maxi, modified by gsyan
                l2 = maxi
            for j in range(len(arr)):
                for k in range(len(arr[0])):
                    if(arr[j][k] >= l1 and arr[j][k] <= l2):
                        brr[j][k]=i
        return brr

    def PNGtoGcode(self,pos_file_png_exported,pos_file_png_BW,pos_file_gcode):
        
        ######## GENERO IMMAGINE IN SCALA DI GRIGI ########
        #Scorro l immagine e la faccio diventare una matrice composta da list


        reader = png.Reader(pos_file_png_exported)#File PNG generato
        
        w, h, pixels, metadata = reader.read_flat()
        
        
        matrice = [[255 for i in range(w)]for j in range(h)]  #List al posto di un array
        

        #Scrivo una nuova immagine in Scala di grigio 8bit
        #copia pixel per pixel 
        
        if self.options.grayscale_type == 1:
            #0.21R + 0.71G + 0.07B
            for y in range(h): # y varia da 0 a h-1
                for x in range(w): # x varia da 0 a w-1
                    pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
                    #matrice[y][x] = int(pixels[pixel_position]*0.21 + pixels[(pixel_position+1)]*0.71 + pixels[(pixel_position+2)]*0.07)                    
                    #
                    # modified by gsyan 
                    # avoid white pixel (255,255,255) to be changed to other color
                    # and find a bug : 0.21+0.71+0.07 != 1
                    #
                    matrice[y][x] = int(round(pixels[pixel_position]*0.21 + pixels[(pixel_position+1)]*0.71 + pixels[(pixel_position+2)]*0.08))

        elif self.options.grayscale_type == 2:
            #(R+G+B)/3
            for y in range(h): # y varia da 0 a h-1
                for x in range(w): # x varia da 0 a w-1
                    pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
                    matrice[y][x] = int((pixels[pixel_position] + pixels[(pixel_position+1)]+ pixels[(pixel_position+2)]) / 3 )        

        elif self.options.grayscale_type == 3:
            #R
            for y in range(h): # y varia da 0 a h-1
                for x in range(w): # x varia da 0 a w-1
                    pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
                    matrice[y][x] = int(pixels[pixel_position])            
                    
        elif self.options.grayscale_type == 4:
            #G
            for y in range(h): # y varia da 0 a h-1
                for x in range(w): # x varia da 0 a w-1
                    pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
                    matrice[y][x] = int(pixels[(pixel_position+1)])    
                    
        elif self.options.grayscale_type == 5:
            #B
            for y in range(h): # y varia da 0 a h-1
                for x in range(w): # x varia da 0 a w-1
                    pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
                    matrice[y][x] = int(pixels[(pixel_position+2)])                

        elif self.options.grayscale_type == 6:
            #Max Color
            for y in range(h): # y varia da 0 a h-1
                for x in range(w): # x varia da 0 a w-1
                    pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
                    list_RGB = pixels[pixel_position] , pixels[(pixel_position+1)] , pixels[(pixel_position+2)]
                    matrice[y][x] = int(max(list_RGB))                

        else:
            #Min Color
            for y in range(h): # y varia da 0 a h-1
                for x in range(w): # x varia da 0 a w-1
                    pixel_position = (x + y * w)*4 if metadata['alpha'] else (x + y * w)*3
                    list_RGB = pixels[pixel_position] , pixels[(pixel_position+1)] , pixels[(pixel_position+2)]
                    matrice[y][x] = int(min(list_RGB))    
        

        ####Ora matrice contiene l'immagine in scala di grigi


        ######## GENERO IMMAGINE IN BIANCO E NERO ########
        #Scorro matrice e genero matrice_BN
        B=255
        N=0 
        
        matrice_BN = [[255 for i in range(w)]for j in range(h)]
        
        
        if self.options.conversion_type == 1:
            #B/W fixed threshold
            soglia = self.options.BW_threshold
            for y in range(h): 
                for x in range(w):
                    if matrice[y][x] >= soglia :
                        matrice_BN[y][x] = B
                    else:
                        matrice_BN[y][x] = N
    
            
        elif self.options.conversion_type == 2:
            #B/W random threshold
            from random import randint
            for y in range(h): 
                for x in range(w): 
                    soglia = randint(20,235)
                    if matrice[y][x] >= soglia :
                        matrice_BN[y][x] = B
                    else:
                        matrice_BN[y][x] = N
            
            
        elif self.options.conversion_type == 3:
            #Halftone
            Step1 = [[B,B,B,B,B],[B,B,B,B,B],[B,B,N,B,B],[B,B,B,B,B],[B,B,B,B,B]]
            Step2 = [[B,B,B,B,B],[B,B,N,B,B],[B,N,N,N,B],[B,B,N,B,B],[B,B,B,B,B]]
            Step3 = [[B,B,N,B,B],[B,N,N,N,B],[N,N,N,N,N],[B,N,N,N,B],[B,B,N,B,B]]
            Step4 = [[B,N,N,N,B],[N,N,N,N,N],[N,N,N,N,N],[N,N,N,N,N],[B,N,N,N,B]]
            
            #for y in range(h/5): 
            for y in range(h//5):  #modified by gsyan  
                #for x in range(w/5): 
                for x in range(w//5):  #modified by gsyan  
                    media = 0
                    for y2 in range(5):
                        for x2 in range(5):
                            media +=  matrice[y*5+y2][x*5+x2]
                    media = media /25
                    for y3 in range(5):
                        for x3 in range(5):
                            if media >= 250 and media <= 255:
                                matrice_BN[y*5+y3][x*5+x3] =     B    
                            if media >= 190 and media < 250:
                                matrice_BN[y*5+y3][x*5+x3] =    Step1[y3][x3]
                            if media >= 130 and media < 190:
                                matrice_BN[y*5+y3][x*5+x3] =    Step2[y3][x3]
                            if media >= 70 and media < 130:
                                matrice_BN[y*5+y3][x*5+x3] =    Step3[y3][x3]
                            if media >= 10 and media < 70:
                                matrice_BN[y*5+y3][x*5+x3] =    Step4[y3][x3]        
                            if media >= 0 and media < 10:
                                matrice_BN[y*5+y3][x*5+x3] = N


        elif self.options.conversion_type == 4:
            #Halftone row
            Step1r = [B,B,N,B,B]
            Step2r = [B,N,N,B,B]
            Step3r = [B,N,N,N,B]
            Step4r = [N,N,N,N,B]

            for y in range(h): 
                # for x in range(w/5): 
                for x in range(w//5): #modified by gsyan
                    media = 0
                    for x2 in range(5):
                        media +=  matrice[y][x*5+x2]
                    media = media /5
                    for x3 in range(5):
                        if media >= 250 and media <= 255:
                            matrice_BN[y][x*5+x3] =     B
                        if media >= 190 and media < 250:
                            matrice_BN[y][x*5+x3] =    Step1r[x3]
                        if media >= 130 and media < 190:
                            matrice_BN[y][x*5+x3] =    Step2r[x3]
                        if media >= 70 and media < 130:
                            matrice_BN[y][x*5+x3] =    Step3r[x3]
                        if media >= 10 and media < 70:
                            matrice_BN[y][x*5+x3] =    Step4r[x3]        
                        if media >= 0 and media < 10:
                            matrice_BN[y][x*5+x3] = N            


        elif self.options.conversion_type == 5:
            #Halftone column
            Step1c = [B,B,N,B,B]
            Step2c = [B,N,N,B,B]
            Step3c = [B,N,N,N,B]
            Step4c = [N,N,N,N,B]

            #for y in range(h/5):
            for y in range(h//5): #modified by gsyan
                for x in range(w):
                    media = 0
                    for y2 in range(5):
                        media +=  matrice[y*5+y2][x]
                    media = media /5
                    for y3 in range(5):
                        if media >= 250 and media <= 255:
                            matrice_BN[y*5+y3][x] =     B
                        if media >= 190 and media < 250:
                            matrice_BN[y*5+y3][x] =    Step1c[y3]
                        if media >= 130 and media < 190:
                            matrice_BN[y*5+y3][x] =    Step2c[y3]
                        if media >= 70 and media < 130:
                            matrice_BN[y*5+y3][x] =    Step3c[y3]
                        if media >= 10 and media < 70:
                            matrice_BN[y*5+y3][x] =    Step4c[y3]        
                        if media >= 0 and media < 10:
                            matrice_BN[y*5+y3][x] = N
        #
        #add by gsyan 
        #
        #code from : 
        #   https://github.com/abhishek-sehgal954/Inkscape_extensions_for_halftone_filters
        #
        elif self.options.conversion_type == 7:
            #Halftone Error diffusion
            matrice_BN = matrice
            for y in range(0,h-1):
                for x in range(1, w-1):
                    neighbour_index = matrice_BN[y][x]
                    if(neighbour_index>127) :
                        matrice_BN[y][x] = 255
                    else :
                        matrice_BN[y][x] = 0
                    diffused_error = neighbour_index - matrice_BN[y][x]
                    matrice_BN[y][x+1] = self.getPixelValidValue( int(matrice_BN[y][x+1] + 7 * diffused_error/16.0) )
                    matrice_BN[y+1][x-1] = self.getPixelValidValue( int(matrice_BN[y+1][x-1] + 3 * diffused_error/16.0) )
                    matrice_BN[y+1][x] = self.getPixelValidValue( int(matrice_BN[y+1][x] + 5 * diffused_error/16.0) )
                    matrice_BN[y+1][x+1] = self.getPixelValidValue( int(matrice_BN[y+1][x+1] + 1 * diffused_error/16.0) )

        elif self.options.conversion_type == 8:
            #Halftone ordered diffusion
            #
            #code from :
            #   https://github.com/abhishek-sehgal954/Inkscape_extensions_for_halftone_filters/blob/master/Raster_to_Raster/ordered_dithering.py
            #			
            arr = matrice
            brr = self.intensity(arr)
            crr = [[8, 3, 4], [6, 1, 2], [7, 5, 9]]
            for y in range(h):
                for x in range(w):
                    if(matrice[y][x] < 255) :
                        if(brr[y][x] > crr[y%3][x%3]):
                            matrice_BN[y][x] = 255
                        else:
                            matrice_BN[y][x] = 0 
                    else :
                        matrice_BN[y][x] = 255 
        
        elif self.options.conversion_type == 9:
            #Halftone Patterning (3x3)
            #
            #code from :
            #   https://github.com/abhishek-sehgal954/Inkscape_extensions_for_halftone_filters/blob/master/Raster_to_Raster/patterning.py
            #
            # based on the intensity maps pixel to the corresponding block of 3*3  
            #  ---   ---   ---   -X-   -XX   -XX   -XX   -XX   XXX   XXX
            #  ---   -X-   -XX   -XX   -XX   -XX   XXX   XXX   XXX   XXX
            #  ---   ---   ---   ---   ---   -X-   -X-   XX-   XX-   XXX
            #  9     8     7     6     5     4     3     2     1     0  
            #  X = 0
            #  - = 255
            #  Therefore intensity 0 being the blackest block.
            matrice_BN = matrice			
            arr = matrice
            brr = self.intensity(arr)
            gray_level = [[[0,0,0],[0,0,0],[0,0,0]] for i in range(10)]
            gray_level[0] = [[0,0,0],[0,0,0],[0,0,0]]
            gray_level[1] = [[0,255,0],[0,0,0],[0,0,0]]
            gray_level[2] = [[0,255,0],[0,0,0],[0,0,255]]
            gray_level[3] = [[255,255,0],[0,0,0],[0,0,255]]
            gray_level[4] = [[255,255,0],[0,0,0],[255,0,255]]
            gray_level[5] = [[255,255,255],[0,0,0],[255,0,255]]
            gray_level[6] = [[255,255,255],[0,0,255],[255,0,255]]
            gray_level[7] = [[255,255,255],[0,0,255],[255,255,255]]
            gray_level[8] = [[255,255,255],[255,0,255],[255,255,255]]
            gray_level[9] = [[255,255,255],[255,255,255],[255,255,255]]
            for y in range(len(brr)//3):
                for x in range(len(brr[y])//3):
                    level = 0
                    for i in range(3):
                        for j in range(3):
                            level = level + brr[y*3+i][x*3+j]
                    level = level//9
                    for i in range(3):
                        for j in range(3):
                            matrice_BN[y*3+i][x*3+j] =  gray_level[level][i][j]
            #crr = numpy.zeros((len(arr)*3,len(arr[0])*3))
            #crr = [[0 for i in range(w*3)]for j in range(h*3)]
            #for y in range(len(brr)):
            #    for x in range(len(brr[y])):
            #        new_y = y+2*(y-1)
            #        new_x = x+2*(x-1)
            #        for i in range(3):
            #            for j in range(3):
            #                #inkex.errormsg([new_y+i , new_x+j, brr[y][x], i, j ])
            #                crr[new_y+i][new_x+j] = gray_level[brr[y][x]][i][j]
            #test_file_png = os.path.join(self.options.directory,"test-zzzz.png") 
            #test_file_img_BN = open(test_file_png, 'wb') #Creo il file
            #test_Costruttore_img = png.Writer(w*3, h*3, greyscale=True, bitdepth=8) #Impostazione del file immagine
            #test_Costruttore_img.write(test_file_img_BN, crr) #Costruttore del file immagine
            #test_file_img_BN.close()    #Chiudo il file
			
        else:
            #Grayscale
            if self.options.grayscale_resolution == 1:
                matrice_BN = matrice
            else:
                for y in range(h): 
                    for x in range(w): 
                        if matrice[y][x] <= 1:
                            # matrice_BN[y][x] == 0
                            matrice_BN[y][x] = 0   #modified by gsyan : correct 'equal' to 'assign'
                            
                        if matrice[y][x] >= 254:
                            # matrice_BN[y][x] == 255
                            matrice_BN[y][x] = 255 #modified by gsyan : correct 'equal' to 'assign'
                        
                        if matrice[y][x] > 1 and matrice[y][x] <254:
                            matrice_BN[y][x] = ( matrice[y][x] // self.options.grayscale_resolution ) * self.options.grayscale_resolution
                        
            
            
        ####Ora matrice_BN contiene l'immagine in Bianco (255) e Nero (0)


        #### SALVO IMMAGINE IN BIANCO E NERO ####
        file_img_BN = open(pos_file_png_BW, 'wb') #Creo il file
        Costruttore_img = png.Writer(w, h, greyscale=True, bitdepth=8) #Impostazione del file immagine
        Costruttore_img.write(file_img_BN, matrice_BN) #Costruttore del file immagine
        file_img_BN.close()    #Chiudo il file


        #### GENERO IL FILE GCODE ####
        if self.options.preview_only == False: #Genero Gcode solo se devo
        
            if self.options.flip_y == False: #Inverto asse Y solo se flip_y = False     
                #-> coordinate Cartesiane (False) Coordinate "informatiche" (True)
                matrice_BN.reverse()                

            ### Replace \n to line feed of laseron & laseroff options . add by gsyan ###
            self.options.laseron = re.sub(r"\\n", '\n', self.options.laseron)
            self.options.laseroff = re.sub(r"\\n", '\n', self.options.laseroff)
            #count variable speed offset
            if self.options.var_speed_on_max > self.options.speed_ON :
                var_speed_offset = (self.options.var_speed_on_max - self.options.speed_ON)//64
            else :
                var_speed_offset = 0
            ### by gsyan End ###
            
            Laser_ON = False
            F_G00 = self.options.speed_OFF  #add by gsyan
            F_G01 = self.options.speed_ON
            Scala = self.options.resolution

            file_gcode = open(pos_file_gcode, 'w')  #Creo il file
            
            #Configurazioni iniziali standard Gcode
            file_gcode.write('; Generated with:\n; "Raster 2 Laser Gcode generator"\n; by 305 Engineering\n;\n;\n;\n')
            
            #Parameter comments, add by gsyan
            #file_gcode.write('; Image file : '+self.args[-1]+'\n')
            file_gcode.write('; Parameters : \n;    resolution : '+str(self.options.resolution)+' pixel/mm\n;    speed : G0 '+str(F_G00)+',  G1 '+ str(F_G01)+(' ' if self.options.conversion_type != 6 or var_speed_offset == 0 else ',  G1 Max '+str(self.options.var_speed_on_max)+' (step '+str(var_speed_offset)+')')+ ('' if self.options.conversion_type != 6 else '\n;    laser power: Max '+str(self.options.laser_max_power)+', Min '+str(self.options.laser_mini_power)) + '\n;\n;\n;\n')
            
            #HOMING
            if self.options.homing == 1:
                file_gcode.write('G28; home all axes\n')
            elif self.options.homing == 2:
                file_gcode.write('$H; home all axes\n')
            else:
                pass
            file_gcode.write('G21; Set units to millimeters\n')            
            file_gcode.write('G90; Use absolute coordinates\n')                
            file_gcode.write('G00 F' + str(F_G00) + '   ; Default Laser Off Speed\n')  # add by gsyan
            file_gcode.write('G01 F' + str(F_G01) + '   ; Default Laser On Speed\n')  # add by gsyan

            #Creazione del Gcode
            
            #allargo la matrice per lavorare su tutta l'immagine
            for y in range(h):
                matrice_BN[y].append(B)
            w = w+1
            
            if self.options.conversion_type != 6:
                for y in range(h):
                    if y % 2 == 0 :
                        for x in range(w):
                            if matrice_BN[y][x] == N :
                                if Laser_ON == False :
                                    file_gcode.write('G00 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G00) + '\n')
                                    # file_gcode.write('G00 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + '\n') #tolto il Feed sul G00
                                    if self.options.laseron_delay > 0:  #add by gsyan
                                        file_gcode.write('G04 P0\n')
                                    file_gcode.write(self.options.laseron + '\n')
                                    if self.options.laseron_delay > 0:  #add by gsyan
                                        file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')
                                    Laser_ON = True
                                if  Laser_ON == True :   #DEVO evitare di uscire dalla matrice
                                    if x == w-1 :
                                        file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G01) + '\n')
                                        if self.options.laseron_delay > 0:  #add by gsyan
                                            file_gcode.write('G04 P0\n')
                                        file_gcode.write(self.options.laseroff + '\n')
                                        Laser_ON = False
                                    else: 
                                        if matrice_BN[y][x+1] != N :
                                            file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G01) +'\n')
                                            if self.options.laseron_delay > 0:  #add by gsyan
                                                file_gcode.write('G04 P0\n')
                                            file_gcode.write(self.options.laseroff + '\n')
                                            Laser_ON = False
                    else:
                        for x in reversed(range(w)):
                            if matrice_BN[y][x] == N :
                                if Laser_ON == False :
                                    file_gcode.write('G00 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G00) + '\n')
                                    #file_gcode.write('G00 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + '\n') #tolto il Feed sul G00
                                    if self.options.laseron_delay > 0:  #add by gsyan
                                        file_gcode.write('G04 P0\n')
                                    file_gcode.write(self.options.laseron + '\n')            
                                    if self.options.laseron_delay > 0:  #add by gsyan
                                        file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')
                                    Laser_ON = True
                                if  Laser_ON == True :   #DEVO evitare di uscire dalla matrice
                                    if x == 0 :
                                        file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G01) + '\n')
                                        if self.options.laseron_delay > 0:  #add by gsyan
                                            file_gcode.write('G04 P0\n')
                                        file_gcode.write(self.options.laseroff + '\n')
                                        Laser_ON = False
                                    else: 
                                        if matrice_BN[y][x-1] != N :
                                            file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G01) +'\n')
                                            if self.options.laseron_delay > 0:  #add by gsyan
                                                file_gcode.write('G04 P0\n')
                                            file_gcode.write(self.options.laseroff + '\n')
                                            Laser_ON = False                

            else: ##SCALA DI GRIGI                
                #add by gsyan : remove power scale (the 'S' parameter) from laser_on option
                re.IGNORECASE = 1  
                
                for y in range(h):
                    if y % 2 == 0 :
                        for x in range(w):
                            if matrice_BN[y][x] != B :
                                if Laser_ON == False :                                
                                    # file_gcode.write('G00 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +'\n')
                                    file_gcode.write('G00 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G00) +'\n') #modified by gsyan
                                    if self.options.laseron_delay > 0:  #add by gsyan
                                        file_gcode.write('G04 P0\n')
                                    #file_gcode.write(self.options.laseron + ' '+ ' S' + str(255 - matrice_BN[y][x]) +'\n')
                                    file_gcode.write( re.sub("(S\d+)", '', self.options.laseron) + ' '+ ' S' + str( self.getLaserPowerValue(255 - matrice_BN[y][x]) ) +'\n')
                                    if self.options.laseron_delay > 0:  #add by gsyan
                                        file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')                                    
                                    Laser_ON = True
                                    
                                if  Laser_ON == True :   #DEVO evitare di uscire dalla matrice
                                    if x == w-1 : #controllo fine riga
                                        file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G01) + '\n')
                                        if self.options.laseron_delay > 0:  #add by gsyan
                                            file_gcode.write('G04 P0\n')
                                        file_gcode.write(self.options.laseroff + '\n')
                                        Laser_ON = False
                                        
                                    else: 
                                        if matrice_BN[y][x+1] == B :
                                            file_gcode.write('G01 X' + str(float(x+1)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G01) +'\n')
                                            if self.options.laseron_delay > 0:  #add by gsyan
                                                file_gcode.write('G04 P0\n')
                                            file_gcode.write(self.options.laseroff + '\n')
                                            Laser_ON = False
                                            
                                        elif matrice_BN[y][x] != matrice_BN[y][x+1] :
                                            if self.options.var_speed_on == False : #add by gsyan
                                                file_gcode.write('G01 X' + str(float(x+1)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G01) +'\n')
                                            else :
                                                #change speed by color ,add by gsyan
                                                file_gcode.write('G01 X' + str(float(x+1)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G01+matrice_BN[y][x]//4*var_speed_offset) + '\n')

                                            if self.options.laseron_delay > 0:  #add by gsyan
                                                file_gcode.write('G04 P0\n')
                                            # file_gcode.write(self.options.laseron + ' '+ ' S' + str(255 - matrice_BN[y][x+1]) +'\n')                                                
                                            file_gcode.write( re.sub("(S\d+)", '', self.options.laseron) + ' '+ ' S' + str( self.getLaserPowerValue( 255 - matrice_BN[y][x+1]) ) +'\n')
                                            if self.options.laseron_delay > 0:  # add by gsyan
                                                file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')
                                            

                    
                    else:
                        for x in reversed(range(w)):
                            if matrice_BN[y][x] != B :
                                if Laser_ON == False :
                                    # file_gcode.write('G00 X' + str(float(x+1)/Scala) + ' Y' + str(float(y)/Scala) +'\n')
                                    file_gcode.write('G00 X' + str(float(x+1)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G00) +'\n')  #modified by gsyan
                                    if self.options.laseron_delay > 0:  #add by gsyan
                                        file_gcode.write('G04 P0\n')
                                    #file_gcode.write(self.options.laseron + ' '+ ' S' + str(255 - matrice_BN[y][x]) +'\n')
                                    file_gcode.write( re.sub("(S\d+)", '', self.options.laseron) + ' '+ ' S' + str( self.getLaserPowerValue( 255 - matrice_BN[y][x] ) ) +'\n')
                                    if self.options.laseron_delay > 0:  #add by gsyan
                                        file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')
                                    Laser_ON = True
                                    
                                if  Laser_ON == True :   #DEVO evitare di uscire dalla matrice
                                    if x == 0 : #controllo fine riga ritorno
                                        file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) +' F' + str(F_G01) + '\n')
                                        if self.options.laseron_delay > 0:  #add by gsyan
                                            file_gcode.write('G04 P0\n')
                                        file_gcode.write(self.options.laseroff + '\n')
                                        Laser_ON = False
                                        
                                    else: 
                                        if matrice_BN[y][x-1] == B :
                                            file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G01) +'\n')
                                            if self.options.laseron_delay > 0:  #add by gsyan
                                                file_gcode.write('G04 P0\n')
                                            file_gcode.write(self.options.laseroff + '\n')
                                            Laser_ON = False
                                            
                                        elif  matrice_BN[y][x] != matrice_BN[y][x-1] :
                                            file_gcode.write('G01 X' + str(float(x)/Scala) + ' Y' + str(float(y)/Scala) + ' F' + str(F_G01) +'\n')
                                            if self.options.laseron_delay > 0:  #add by gsyan
                                                file_gcode.write('G04 P0\n')
                                            # file_gcode.write(self.options.laseron + ' '+ ' S' + str(255 - matrice_BN[y][x-1]) +'\n')
                                            file_gcode.write( re.sub("(S\d+)", '', self.options.laseron) + ' '+ ' S' + str( self.getLaserPowerValue( 255 - matrice_BN[y][x-1]) ) +'\n')
                                            if self.options.laseron_delay > 0:  #add by gsyan
                                                file_gcode.write('G04 P' + str(self.options.laseron_delay) + '\n')

            
            
            #Configurazioni finali standard Gcode
            #file_gcode.write('G00 X0 Y0; home\n')  #modified by gsyan , add travel speed
            file_gcode.write('G00 X0 Y0' + ' F' + str(F_G00)+ ' ; home\n')
            #HOMING
            if self.options.homing == 1:
                file_gcode.write('G28; home all axes\n')
            elif self.options.homing == 2:
                file_gcode.write('$H; home all axes\n')
            else:
                pass
            
            file_gcode.close() #Chiudo il file




########     ########     ########     ########     ########     ########     ########     ########     ########     


def _main():
    e=GcodeExport()
    if hasattr(e, "run") :
        #
        # for Inkscape 1.x
        #    
        e.run() #modified by gsyan
    else :
        #
        # for Inkscape 0.92
        #    
        e.affect()
    

    exit()

if __name__=="__main__":
    _main()




