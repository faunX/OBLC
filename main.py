from distutils.command.config import config
import os
from threading import Thread
from time import sleep
import requests
from flask import Flask
import json
from Configuration import Configuration
from buildingPipeline import BuildingPipeline
from logger import OBLC_Logger
import wrapper.interractorWrapper as InterractorWrapper

class OBLC:
    #INTERRACTOR_IP = '127.0.0.1'
    #INTERRACTOR_PORT = '8080'
    #status = 'normal'
    #RESOURCE_LIMITER_URL = 'http://127.0.0.1:5000'
    #BUILDING_MANAGER_URL ='http://127.0.0.1:5001'
    #LOG_LEVEL = 'Info'

    def __init__(self):
        self.logger = OBLC_Logger('Init')
        self.config = self.setup()

        self.interractor = InterractorWrapper.Interractor(self.config.INTERRACTOR_IP, self.config.INTERRACTOR_PORT)
        self.buildingPipeline = BuildingPipeline(self.interractor, self.logger, self.config)
        self.resumeBuildPipeline()

        self.runBody()

    def setVariableFromEnvVar(self, defaultValue, envVarName):
        envValue = os.environ.get(envVarName)
        if envValue is not None:
            self.logger.log(f'{envVarName} is {envValue}', 'WARN')
            return envValue
        else:
            self.logger.log(f'{envVarName} not found returning default: {defaultValue}','WARN')
            return defaultValue

    def setup(self):
        config = Configuration()
        config.INTERRACTOR_IP = self.setVariableFromEnvVar(config.INTERRACTOR_IP, 'INTERRACTOR_IP')
        config.INTERRACTOR_PORT = self.setVariableFromEnvVar(config.INTERRACTOR_PORT, 'INTERRACTOR_PORT')
        config.RESOURCE_LIMITER_ADDR = self.setVariableFromEnvVar(config.RESOURCE_LIMITER_ADDR, 'RESOURCE_LIMITER_URL')
        config.BUILDING_MANAGER_ADDR = self.setVariableFromEnvVar(config.BUILDING_MANAGER_ADDR, 'BUILDING_MANAGER_URL')
        config.LOG_LEVEL = self.setVariableFromEnvVar(config.LOG_LEVEL, 'OGAME_LOG_LEVEL')

        self.logger.setLogLevel(config.LOG_LEVEL)

        return config

    def resumeBuildPipeline(self):
        thread = Thread(target=self.buildingPipeline.resume)
        thread.start()

        self.isAttackPipelineResumed = False

    def pauseBuildPipeline(self):
        self.buildingPipeline.pause()
        #self.isAttackPipelineResumed = True

    def runBody(self):
        counter = 0
        while(True):
            print("MAIN started2")
            counter = counter + 1
            if(counter == 3):
                self.pauseBuildPipeline()
                print("paused for some time")
                sleep(10)
                self.resumeBuildPipeline()
            sleep(4)

oblc = OBLC()

    #respPlanets = interractor.planets()
    #for planet in respPlanets:
        #planetID = planet['ID']
        #executePipeline(planetID)


    #interractor.ships(33637224)



    #interractor.build(33637224,4,1)
    #sleep(2)
    #interractor.cancelBuild(33637224,4)
    #interractor.resources(33637224)


    #interractor.resourceBuildings(33637224)