import json,click
import requests
from ruxit.api.base_plugin import RemoteBasePlugin
import logging
import check_tls_certs
import datetime
import os
from ruxit.api.data import StatCounterDataPoint

logger = logging.getLogger(__name__)


class CertsPluginRemote(RemoteBasePlugin):
    
    def initialize(self, **kwargs):
        config = kwargs['config']
        logger.info("Config: %s", config)
        self.path = os.getcwd()
        self.period = config["period"]
        self.default_expiry_warn = self.period
        self.domains = list(check_tls_certs.itertools.chain(
        check_tls_certs.domain_definitions_from_filename(self.path + "/hosts.txt")))
        self.domain_certs = check_tls_certs.get_domain_certs(self.domains)
        self.exceptions = list(x for x in self.domain_certs.values() if isinstance(x, Exception))
        self.total_warnings = 0
        self.total_errors = 0
        self.earliest_expiration = None
        self.utcnow = datetime.datetime.utcnow()
        self.checked_domains = check_tls_certs.check_domains(self.domains, self.domain_certs, self.utcnow, expiry_warn=self.default_expiry_warn)
        print(self.checked_domains)
       
        for domainnames, msgs, expiration in self.checked_domains:
            if expiration:
                print("expiration: " + str(expiration))
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
          
       

    def query(self, **kwargs):
        # Create group - provide group id used to calculate unique entity id in dynatrace
        #   and display name for UI presentation
        group = self.topology_builder.create_group(identifier="CertGroup",
                                                   group_name="SSL Expiration Group")

        # Create device - provide device id used to calculate unique entity id in dynatrace
        #   and display name for UI presentation
        #device = group.create_device(identifier="SSLDevice",
        #                            display_name="SSL Device")

        
        

        # Push infrastructure problems
       
        for domainnames, msgs, expiration in self.checked_domains:
            if expiration:
                print("expiration: " + str(expiration))
                if self.earliest_expiration is None or expiration < self.earliest_expiration:
                   self.earliest_expiration = expiration
            warnings = 0
            errors = 0
            domain_msgs = [', '.join(domainnames)]
            print("domainnames: ", domainnames)
            for level, msg in msgs:
                if level == 'warning' and "The certificate expires" in msg:
                    logger.info("Logging Problem for Domain:%s, Warning:%s", domainnames,msg)
                    device = group.create_device(identifier= domainnames[0],
                                                 display_name=domainnames[0])
                    logger.info("Topology: group name=%s, node name=%s", group.name, device.name)
                    device.report_error_event(title="Certificate Expiration Within " + str(self.default_expiry_warn) + " days",
                                description="The SSL Cerficate is about to expire.",
                                properties={"exp_Date": str(expiration)})

        # Report problems
        """
        device.report_performance_event(title="Performance Event",
                                      description="Use it to focus on some performance issue",
                                      properties={"property_key": "property_value"})

        device.report_error_event(title="Error Event",
                                description="Use it to report some error",
                                properties={"property_key": "property_value"})
        logger.info("Report error event")

        device.report_availability_event(title="Availability Event",
                                       description="Use it to focus on some availability issue",
                                       properties={"property_key": "property_value"})
        logger.info("Report availability event")

        device.report_resource_contention_event(title="Resources Contention Event",
                                              description="Use it to focus on some resource contention issue",
                                              properties={"property_key": "property_value"})
        logger.info("Report resource contention event")

        # report information
        device.report_custom_info_event(title="Custom Info Event",
                                      description="Use it to report some custom info",
                                      properties={"property_key": "property_value"})
        logger.info("Report custom info event")

        device.report_custom_deployment_event(source="demo source",
                                            project="demo plugin",
                                            version="1.001",
                                            ci_link=self.url + "/deployment",
                                            remediation_action_link=self.url + "/remediation",
                                            deployment_name="Demo deployment",
                                            properties={"property_key": "property_value"})
        logger.info("Report custom deployment event")

        device.report_custom_annotation_event(description="Annotation event",
                                            annotation_type="demo",
                                            source="demo source",
                                            properties={"property_key": "property_value"})
        logger.info("Report custom annotation event")
"""