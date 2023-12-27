import platform
import numpy as np
import metacv as mc

if platform.machine() == 'aarch64':
    from hobot_dnn import pyeasy_dnn as HB
else:
    from horizon_tc_ui import HB_ONNXRuntime as HB

Detection = mc.Detection


class DetectionHB(Detection):
    def __init__(self,
                 model_path: str,
                 input_width: int,
                 input_height: int,
                 confidence_thresh: float,
                 nms_thresh: float,
                 class_names: list,
                 device_id=0):
        super().__init__(model_path, input_width, input_height, confidence_thresh, nms_thresh, class_names)
        self.device_id = device_id
        self.model = None
        self.det_output = None
        self.input_names = None
        self.output_names = None
        self.initialize_model()

    def convert_and_load(self,
                         quantize=False,
                         dataset='dataset.txt',
                         is_hybrid=False,
                         output_names=["output0", "output1"]):
        pass

    def initialize_model(self):
        if platform.machine() == 'aarch64':
            hb = HB.load(self.model_path)[0]
        else:
            hb = HB(self.model_path)
            self.input_names = hb.input_names
            self.output_names = hb.output_names

        self.model = hb

    def infer(self, image):
        # 由继承类实现模型推理
        input_tensor = image[np.newaxis, :, :, :].astype(np.uint8)
        if platform.machine() == 'aarch64':
            outputs = self.model.forward(input_tensor)
            self.det_output = np.squeeze(outputs[0].buffer).T
        else:
            outputs = self.model.run(self.output_names, {self.input_names[0]: input_tensor}, input_offset=128)
            self.det_output = np.squeeze(outputs[0]).T
