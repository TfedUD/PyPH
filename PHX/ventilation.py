import PHX._base
import PHX.utilization_patterns
import PHX.ventilation_components
import PHX.hvac


class AirflowRates(PHX._base._Base):
    def __init__(self):
        super(AirflowRates, self).__init__()
        self.supply = 0.0
        self.extract = 0.0
        self.transfer = 0.0

    def join(self, _other):
        """Returns a new airflow object with the maximum values from each input"""
        new_obj = self.__class__()

        new_obj.supply = max(self.supply, _other.supply)
        new_obj.extract = max(self.extract, _other.extract)
        new_obj.transfer = max(self.transfer, _other.transfer)

        return new_obj

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._AirflowRates(cls, _dict)

    def __repr__(self):
        return "{}(supply={:.02f}, extract={:.02f}, transfer={:.02f})".format(
            self.__class__.__name__, self.supply, self.extract, self.transfer
        )

    def __str__(self):
        return self.__repr__()


class SpaceVentilation(PHX._base._Base):

    _count = 0

    def __init__(self):
        self.id = self._count
        super(SpaceVentilation, self).__init__()
        self.airflow_rates = AirflowRates()
        self.utilization = PHX.utilization_patterns.UtilPat_Vent.default()
        self.system = PHX.ventilation_components.Ventilation_System.default()

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._SpaceVentilation(cls, _dict)

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(SpaceVentilation, cls).__new__(cls, *args, **kwargs)

    def __add__(self, _other):
        new_obj = self.__class__()

        new_obj.airflow_rates = self.airflow_rates.join(_other.airflow_rates)

        #
        #
        # TODO: Join Utilizations
        #
        #
        # TODO: Join Systems
        #
        #

        return new_obj
