import math


class LLT:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ChinaGeocoordTrans:
    def __init__(self):
        self.__pi = 3.1415926535897932384626  # π
        self.__x_pi = self.__pi * 3000.0 / 180.0
        self.__a = 6378245.0  # 长半轴
        self.__ee = 0.00669342162296594323  # 偏心率平方
        # 百度墨卡托投影纠正矩阵
        self.LLBAND = [75, 60, 45, 30, 15, 0]
        self.LL2MC = [
            [-0.0015702102444, 111320.7020616939, 1704480524535203, -10338987376042340, 26112667856603880,
             -35149669176653700,
             26595700718403920, -10725012454188240, 1800819912950474, 82.5],
            [0.0008277824516172526, 111320.7020463578, 647795574.6671607, -4082003173.641316, 10774905663.51142,
             -15171875531.51559, 12053065338.62167, -5124939663.577472, 913311935.9512032, 67.5],
            [0.00337398766765, 111320.7020202162, 4481351.045890365, -23393751.19931662, 79682215.47186455,
             -115964993.2797253,
             97236711.15602145, -43661946.33752821, 8477230.501135234, 52.5],
            [0.00220636496208, 111320.7020209128, 51751.86112841131, 3796837.749470245, 992013.7397791013,
             -1221952.21711287,
             1340652.697009075, -620943.6990984312, 144416.9293806241, 37.5],
            [-0.0003441963504368392, 111320.7020576856, 278.2353980772752, 2485758.690035394, 6070.750963243378,
             54821.18345352118, 9540.606633304236, -2710.55326746645, 1405.483844121726, 22.5],
            [-0.0003218135878613132, 111320.7020701615, 0.00369383431289, 823725.6402795718, 0.46104986909093,
             2351.343141331292, 1.58060784298199, 8.77738589078284, 0.37238884252424, 7.45]]
        # 百度墨卡托转回到百度经纬度纠正矩阵
        self.MCBAND = [12890594.86, 8362377.87, 5591021, 3481989.83, 1678043.12, 0]
        self.MC2LL = [
            [1.410526172116255e-8, 0.00000898305509648872, -1.9939833816331, 200.9824383106796, -187.2403703815547,
             91.6087516669843, -23.38765649603339, 2.57121317296198, -0.03801003308653, 17337981.2],
            [-7.435856389565537e-9, 0.000008983055097726239, -0.78625201886289, 96.32687599759846,
             -1.85204757529826,
             -59.36935905485877, 47.40033549296737, -16.50741931063887, 2.28786674699375, 10260144.86],
            [-3.030883460898826e-8, 0.00000898305509983578, 0.30071316287616, 59.74293618442277, 7.357984074871,
             -25.38371002664745, 13.45380521110908, -3.29883767235584, 0.32710905363475, 6856817.37],
            [-1.981981304930552e-8, 0.000008983055099779535, 0.03278182852591, 40.31678527705744, 0.65659298677277,
             -4.44255534477492, 0.85341911805263, 0.12923347998204, -0.04625736007561, 4482777.06],
            [3.09191371068437e-9, 0.000008983055096812155, 0.00006995724062, 23.10934304144901, -0.00023663490511,
             -0.6321817810242, -0.00663494467273, 0.03430082397953, -0.00466043876332, 2555164.4],
            [2.890871144776878e-9, 0.000008983055095805407, -3.068298e-8, 7.47137025468032, -0.00000353937994,
             -0.02145144861037, -0.00001234426596, 0.00010322952773, -0.00000323890364, 826088.5]]

    def bd09_to_gcj02(self, bd_lon, bd_lat):
        """
        百度坐标系(BD-09)转火星坐标系(GCJ-02)
        百度——>谷歌、高德
        :param bd_lat:百度坐标纬度
        :param bd_lon:百度坐标经度
        :return:转换后的坐标列表形式
        """
        x = bd_lon - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * self.__x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * self.__x_pi)
        gg_lng = round(z * math.cos(theta), 6)
        gg_lat = round(z * math.sin(theta), 6)
        return [gg_lng, gg_lat]

    def gcj02_to_wgs84(self, lng, lat):
        """
        GCJ02(火星坐标系)转GPS84
        :param lng:火星坐标系的经度
        :param lat:火星坐标系纬度
        :return:
        """
        if self.__out_of_china(lng, lat):
            return [lng, lat]
        dlat = self.__transformlat(lng - 105.0, lat - 35.0)
        dlng = self.__transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.__pi
        magic = math.sin(radlat)
        magic = 1 - self.__ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.__a * (1 - self.__ee)) / (magic * sqrtmagic) * self.__pi)
        dlng = (dlng * 180.0) / (self.__a / sqrtmagic * math.cos(radlat) * self.__pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [round(lng * 2 - mglng, 6), round(lat * 2 - mglat, 6)]

    def bd09_to_wgs84(self, bd_lon, bd_lat):
        lon, lat = self.bd09_to_gcj02(bd_lon, bd_lat)
        return self.gcj02_to_wgs84(lon, lat)

    def gcj02_to_bd09(self, lng, lat):
        """
        火星坐标系(GCJ-02)转百度坐标系(BD-09)
        谷歌、高德——>百度
        :param lng:火星坐标经度
        :param lat:火星坐标纬度
        :return:
        """
        z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * self.__x_pi)
        theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * self.__x_pi)
        bd_lng = round(z * math.cos(theta) + 0.0065, 6)
        bd_lat = round(z * math.sin(theta) + 0.006, 6)
        return [bd_lng, bd_lat]

    def wgs84_to_gcj02(self, lng, lat):
        """
        WGS84转GCJ02(火星坐标系)
        :param lng:WGS84坐标系的经度
        :param lat:WGS84坐标系的纬度
        :return:
        """
        if self.__out_of_china(lng, lat):  # 判断是否在国内
            return [lng, lat]
        dlat = self.__transformlat(lng - 105.0, lat - 35.0)
        dlng = self.__transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.__pi
        magic = math.sin(radlat)
        magic = 1 - self.__ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.__a * (1 - self.__ee)) / (magic * sqrtmagic) * self.__pi)
        dlng = (dlng * 180.0) / (self.__a / sqrtmagic * math.cos(radlat) * self.__pi)
        mglat = round(lat + dlat, 6)
        mglng = round(lng + dlng, 6)
        return [mglng, mglat]

    def wgs84_to_bd09(self, lon, lat):
        lon, lat = self.wgs84_to_gcj02(lon, lat)
        return self.gcj02_to_bd09(lon, lat)

    def __out_of_china(self, lng, lat):
        """
        判断是否在国内，不在国内不做偏移
        :param lng:
        :param lat:
        :return:
        """
        return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

    def __transformlng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
              0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.__pi) + 20.0 *
                math.sin(2.0 * lng * self.__pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.__pi) + 40.0 *
                math.sin(lng / 3.0 * self.__pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.__pi) + 300.0 *
                math.sin(lng / 30.0 * self.__pi)) * 2.0 / 3.0
        return ret

    def __transformlat(self, lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
              0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.__pi) + 20.0 *
                math.sin(2.0 * lng * self.__pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.__pi) + 40.0 *
                math.sin(lat / 3.0 * self.__pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.__pi) + 320 *
                math.sin(lat * self.__pi / 30.0)) * 2.0 / 3.0
        return ret

    def wgs84tomercator(self, lng, lat):
        """
        wgs84投影到墨卡托
        :param lng:
        :param lat:
        :return:
        """
        x = round(lng * 20037508.34 / 180, 7)
        y = round(math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180) * 20037508.34 / 180, 7)
        return x, y

    def mercatortowgs84(self, x, y):
        """
        墨卡托投影坐标转回wgs84
        :param x:
        :param y:
        :return:
        """
        lng = round(x / 20037508.34 * 180, 6)
        lat = round(180 / math.pi * (2 * math.atan(math.exp(y / 20037508.34 * 180 * math.pi / 180)) - math.pi / 2), 6)
        return lng, lat

    def __getrange(self, cC, cB, T):
        if (cB != None):
            cC = max(cC, cB)
        if (T != None):
            cC = min(cC, T)
        return cC

    def __getloop(self, cC, cB, T):
        while (cC > T):
            cC -= T - cB
        while (cC < cB):
            cC += T - cB
        return cC

    def __convertor(self, cC, cD):
        if (cC == None or cD == None):
            print('null')
            return None
        T = cD[0] + cD[1] * abs(cC.x)
        cB = abs(cC.y) / cD[9]
        cE = cD[2] + cD[3] * cB + cD[4] * cB * cB + cD[5] * cB * cB * cB + cD[6] * cB * cB * cB * cB + cD[
            7] * cB * cB * cB * cB * cB + cD[8] * cB * cB * cB * cB * cB * cB
        if (cC.x < 0):
            T = T * -1
        else:
            T = T
        if (cC.y < 0):
            cE = cE * -1
        else:
            cE = cE
        return [T, cE]

    def __convertLL2MC(self, T):
        cD = None
        T.x = self.__getloop(T.x, -180, 180)
        T.y = self.__getrange(T.y, -74, 74)
        cB = T
        for cC in range(0, len(self.LLBAND), 1):
            if (cB.y >= self.LLBAND[cC]):
                cD = self.LL2MC[cC]
                break
        if (cD != None):
            for cC in range(len(self.LLBAND) - 1, -1, -1):
                if (cB.y <= -self.LLBAND[cC]):
                    cD = self.LL2MC[cC]
                    break
        cE = self.__convertor(T, cD)
        cE = [round(c, 7) for c in cE]
        return cE

    def __convertMC2LL(self, cB):
        cC = LLT(abs(cB.x), abs(cB.y))
        cE = None
        for cD in range(0, len(self.MCBAND), 1):
            if (cC.y >= self.MCBAND[cD]):
                cE = self.MC2LL[cD]
                break
        T = self.__convertor(cB, cE)
        T = [round(c, 6) for c in T]
        return T

    def bd09tomercator(self, lng, lat):
        """
        bd09投影到百度墨卡托
        :param lng:
        :param lat:
        :return:
        """
        baidut = LLT(lng, lat)
        return self.__convertLL2MC(baidut)

    def mercatortobd09(self, x, y):
        """
        墨卡托投影坐标转回bd09
        :param x:
        :param y:
        :return:
        """
        baidut = LLT(x, y)
        return self.__convertMC2LL(baidut)


if __name__ == '__main__':
    trans = ChinaGeocoordTrans()
    p_mercator = [(12949466.756021, 4824984.030953), (12949654.450512, 4825246.444941)]
    print(p_mercator)
    p_bd09 = [trans.mercatortobd09(*p) for p in p_mercator]
    print(p_bd09)

    _p_mercator = [trans.bd09tomercator(*p) for p in p_bd09]
    print(_p_mercator)

    _p_bd09 = [trans.mercatortobd09(*p) for p in _p_mercator]
    print(_p_bd09)

    _p_wgs = [trans.bd09_to_wgs84(*p) for p in p_bd09]
    print(_p_wgs)

    _p_gcj02 = [trans.wgs84_to_gcj02(*p) for p in _p_wgs]
    print(_p_gcj02)

    _p_bd09 = [trans.gcj02_to_bd09(*p) for p in _p_gcj02]
    print(_p_bd09)
