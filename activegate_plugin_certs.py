"""
 * Copyright 2019. Mediro-ICT and its affiliates.
 * All Rights Reserved.
 * This is unpublished proprietary source code of Mediro-ICT and its affiliates.
 * The copyright notice above does not evidence any actual or intended publication of such source code.
 *
"""

import json,click
import requests
from ruxit.api.base_plugin import RemoteBasePlugin
import logging
import check_tls_certs
import datetime 
from datetime import datetime as timedelta
import os
from ruxit.api.data import StatCounterDataPoint

logger = logging.getLogger(__name__)


class CertsPluginRemote(RemoteBasePlugin):
    
    def initialize(self, **kwargs):
        config = kwargs['config']
        logger.info("Config: %s", config)
        self.path = os.getcwd()
        self.period = config["period"]
        self.alert_period = config["alert_period"]
        self.poll_period = config["poll_interval"]
        self.event_type = config["event_type"]
        self.show_checks = config["show_checks"]
        self.hosts = config["hosts"].split(",")
        self.default_expiry_warn = self.period
        self.default_expiry_err = self.alert_period
        
        #self.alert_interval = self.config.get("alert_interval")
        #self.event_interval = self.config.get("event_interval")
        
        

        self.alert_iterations = 0
        self.event_iterations = 0
        self.absolute_iterations = 0
        

        self.current_entries = 1
        self.archived_entries = 0




        self.domains = None

        

        
    



        
          
       

    def query(self, **kwargs):
        # Create group - provide group id used to calculate unique entity id in dynatrace
        #   and display name for UI presentation

        if self.should_poll_cert():
            self.poll_hosts()
        else:
            logger.info("Hosts not being polled:%s < %s",self.absolute_iterations, self.poll_period)

        for domainnames, msgs, expiration in self.checked_domains:
            if expiration:
                print("expiration1: " + str(expiration))
                if self.earliest_expiration is None or expiration < self.earliest_expiration:
                   self.earliest_expiration = expiration
            warnings = 0
            errors = 0
            domain_msgs = [', '.join(domainnames)]
            for level, msg in msgs:
                if level == 'error':
                   color = 'red'
                   errors = errors + 1
                elif level == 'warning':
                   color = 'yellow'
                   warnings = warnings + 1
                else:
                   color = None
                if color:
                   msg = click.style(msg, fg=color)
                msg = "\n".join("    " + m for m in msg.split('\n'))
                domain_msgs.append(msg)
       
            if warnings or errors:
               click.echo('\n'.join(domain_msgs))

            self.total_errors = self.total_errors + errors
            self.total_warnings = self.total_warnings + warnings
            msg = "%s error(s), %s warning(s)" % (self.total_errors, self.total_warnings)
   
            if self.earliest_expiration:
               msg += "\nEarliest expiration on %s (%s)." % (
               self.earliest_expiration, self.earliest_expiration - self.utcnow)
            if len(self.exceptions) > (len(self.domain_certs.values()) / 2):
              click.echo(click.style(msg, fg="red"))
         
        if self.total_errors:
            click.echo(click.style(msg, fg="red"))
          
        elif self.total_warnings:
            click.echo(click.style(msg, fg="yellow"))    
        
        group = self.topology_builder.create_group(identifier="CertGroup",
                                                   group_name="SSL Expiration Group")

        # Create device - provide device id used to calculate unique entity id in dynatrace
        #   and display name for UI presentation
        #device = group.create_device(identifier="SSLDevice",
        #                            display_name="SSL Device")

        def days_between(d2):
            #d1 = datetime.strptime(d1, "%Y-%m-%d")
            d1 = datetime.datetime.utcnow().date()
            d2 = datetime.datetime.strptime(d2, '%Y-%m-%d %H:%M:%S').date()
            return str(abs((d2 - d1).days))  
        

        # Push infrastructure info events and problems
        
        for domainnames, msgs, expiration in self.checked_domains:
            if expiration:
                
                if self.earliest_expiration is None or expiration < self.earliest_expiration:
                   self.earliest_expiration = expiration
                print("expiration: " + str(expiration))   
            warnings = 0
            errors = 0
            domain_msgs = [', '.join(domainnames)]
            print("domainnames: ", domainnames)
            #days = days_between(str(expiration))
            for level, msg in msgs:
                
                    
                
                if level == 'warning' and "The certificate expires" in msg:
                   
                    days = days_between(str(expiration))
                    
                    device = group.create_device(identifier= domainnames[0],
                                                 display_name=domainnames[0])
                    if (self.absolute_iterations ==1):
                        
                        print("Iterations: ", self.absolute_iterations)
                        if int(days) > int(self.default_expiry_err) and int(days) <= int(self.default_expiry_warn):
                            logger.info("Logging Warning Event for Domain:%s, Warning:%s", domainnames,msg)
                            
                            if self.event_type == "Custom Info":
                                device.report_custom_info_event(title="WARNING:Certificate Expiration Within the Warning threshold set: " + str(self.default_expiry_warn) + " days",
                                      description="The SSL Cerficate  will expire in: "+ days + " days",
                                      properties={"exp_date": str(expiration),
                                                  "exp_days": str(days)
                                      
                                      }
                                      )
                                logger.info("Custom Event:%s, Warning:%s", domainnames,msg)

                            if self.event_type == "Error":
                                device.report_error_event(title="WARNING:Certificate Expiration Within the Warning threshold set: " + str(self.default_expiry_warn) + " days",
                                      description="The SSL Cerficate  will expire in: "+ days + " days",
                                      properties={"exp_date": str(expiration),
                                                  "exp_days": str(days)   
                                      }
                                      )
                                logger.info("Error Event:%s, Warning:%s", domainnames,msg)

                        elif int(days) <= int(self.default_expiry_err):
                            logger.info("Logging Problem Alert for Domain:%s, Warning:%s", domainnames,msg)
                            logger.info("Topology: group name=%s, node name=%s", group.name, device.name)
                            device.report_error_event(title="ERROR:Certificate Expiration Within the Alert threshold set: " + str(self.default_expiry_err) + " days",
                                description="The SSL Cerficate  will expire in: "+ days + " days",
                                properties={"exp_date": str(expiration),
                                             "exp_days": str(days)
                                }
                                
                                )
                               
                    else:
                        logger.info("Event not being logged to prevent spam:%s",self.absolute_iterations)
                        
                       
                elif "Valid until" in msg and self.show_checks == True and self.absolute_iterations ==1:
                    days = days_between(str(expiration))
                    if int(days) > int(self.default_expiry_warn):
                        device = group.create_device(identifier= domainnames[0],display_name=domainnames[0])
                        device.report_custom_annotation_event(description="Certificate for "+ domainnames[0] +" Checked",source=msg)
                        print(self.absolute_iterations)
                
                elif "The certificate has expired" in msg and self.absolute_iterations ==1:
                    device = group.create_device(identifier= domainnames[0],display_name=domainnames[0])
                    logger.info("Logging Problem Alert for Domain:%s, Warning:%s", domainnames,msg)
                    logger.info("Topology: group name=%s, node name=%s", group.name, device.name)
                    
                    device.report_error_event(title="CRITICAL:SSL Certificate has expired",
                                description="The SSL Certificate has expired",
                                properties={"exp_date": str(expiration)})
                else:
                    logger.info("error occured:%s",msg)   

                    
                     


    
    def poll_hosts(self):
        if (not self.hosts.count("") > 0 and self.hosts is not None):
            logger.info("Polling %s hosts",len(self.hosts))
            self.domains = list(check_tls_certs.itertools.chain(
                check_tls_certs.domain_definitions_from_cli(self.hosts)))
            logger.info("Using Host list from plugin config:%s",self.hosts)
            
        else:
            self.domains = list(check_tls_certs.itertools.chain(
                check_tls_certs.domain_definitions_from_filename(self.path + "/hosts.txt")))
            logger.info("Using Host list from hosts.txt file")    
     
        logger.info("Iterations:%s",self.absolute_iterations)
        
        self.domain_certs = check_tls_certs.get_domain_certs(self.domains)
        self.exceptions = list(x for x in self.domain_certs.values() if isinstance(x, Exception))
        self.total_warnings = 0
        self.total_errors = 0
        self.earliest_expiration = None
        self.utcnow = datetime.datetime.utcnow()
        self.checked_domains = check_tls_certs.check_domains(self.domains, self.domain_certs, self.utcnow, expiry_warn=self.default_expiry_warn)
           
        print("Checked Domains:", self.checked_domains)
        

        
    
    
    def should_poll_cert(self):
        self.absolute_iterations = self.absolute_iterations + 1
        
        if (self.absolute_iterations > self.poll_period):
            self.absolute_iterations = 0
            return True

        if self.absolute_iterations ==1:
             return True   

        return False   
    """
    def should_create_event(self):
        self.event_iterations = self.event_iterations + 1
        if self.event_iterations > self.event_interval:
            self.event_iterations = 0
            return True
        return False    

    def should_create_error(self):
        self.alert_iterations = self.alert_iterations + 1
        if self.alert_iterations > self.alert_interval:
            self.alert_iterations = 0
            return True
        return False    
   """
               