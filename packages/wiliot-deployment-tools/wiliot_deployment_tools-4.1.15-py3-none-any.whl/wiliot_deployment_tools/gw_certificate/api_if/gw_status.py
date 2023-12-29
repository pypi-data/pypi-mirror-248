from dataclasses import dataclass

@dataclass
class GWCapabilities:
    tagMetadataCouplingSupported:bool = False
    downlinkSupported:bool = False
    bridgeOtaUpgradeSupported:bool = False
    fwUpgradeSupported:bool = False
    geoLocationSupport:bool = False
    
    @staticmethod
    def get_capabilities():
        return list(GWCapabilities.__dataclass_fields__.keys())
print(GWCapabilities.get_capabilities())