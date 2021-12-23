from utils.apiResponse import ApiResponse
from anomaly.models import DetectionRuleType
from anomaly.serializers import DetectionRuleTypeSerializer


class DetectionRules:
    """
    Services for Detection Rules
    """

    @staticmethod
    def getDetectionRuleTypes():
        """
        Gets all detection rule types
        """
        res = ApiResponse()
        data = DetectionRuleTypeSerializer(DetectionRuleType.objects.all(), many=True).data
        res.update(True, "Successfully retrieved detection rule types", data)
        return res


