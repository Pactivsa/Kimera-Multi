# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from data_package/LinktrackNodeframe2.msg. Do not edit."""
import codecs
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import data_package.msg
import genpy

class LinktrackNodeframe2(genpy.Message):
  _md5sum = "770370fbc0ccd2da0f93103d836d1060"
  _type = "data_package/LinktrackNodeframe2"
  _has_header = False  # flag to mark the presence of a Header object
  _full_text = """uint8 role
uint8 id
time stamp
uint32 local_time
uint32 system_time
float32 voltage
float32[3] pos_3d
float32[3] eop_3d
float32[3] vel_3d
float32[3] angle_3d
float32[4] quaternion
float32[3] imu_gyro_3d
float32[3] imu_acc_3d
LinktrackNode2[] nodes

================================================================================
MSG: data_package/LinktrackNode2
uint8 role
uint8 id
float32 dis
float32 fp_rssi
float32 rx_rssi
"""
  __slots__ = ['role','id','stamp','local_time','system_time','voltage','pos_3d','eop_3d','vel_3d','angle_3d','quaternion','imu_gyro_3d','imu_acc_3d','nodes']
  _slot_types = ['uint8','uint8','time','uint32','uint32','float32','float32[3]','float32[3]','float32[3]','float32[3]','float32[4]','float32[3]','float32[3]','data_package/LinktrackNode2[]']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       role,id,stamp,local_time,system_time,voltage,pos_3d,eop_3d,vel_3d,angle_3d,quaternion,imu_gyro_3d,imu_acc_3d,nodes

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(LinktrackNodeframe2, self).__init__(*args, **kwds)
      # message fields cannot be None, assign default values for those that are
      if self.role is None:
        self.role = 0
      if self.id is None:
        self.id = 0
      if self.stamp is None:
        self.stamp = genpy.Time()
      if self.local_time is None:
        self.local_time = 0
      if self.system_time is None:
        self.system_time = 0
      if self.voltage is None:
        self.voltage = 0.
      if self.pos_3d is None:
        self.pos_3d = [0.] * 3
      if self.eop_3d is None:
        self.eop_3d = [0.] * 3
      if self.vel_3d is None:
        self.vel_3d = [0.] * 3
      if self.angle_3d is None:
        self.angle_3d = [0.] * 3
      if self.quaternion is None:
        self.quaternion = [0.] * 4
      if self.imu_gyro_3d is None:
        self.imu_gyro_3d = [0.] * 3
      if self.imu_acc_3d is None:
        self.imu_acc_3d = [0.] * 3
      if self.nodes is None:
        self.nodes = []
    else:
      self.role = 0
      self.id = 0
      self.stamp = genpy.Time()
      self.local_time = 0
      self.system_time = 0
      self.voltage = 0.
      self.pos_3d = [0.] * 3
      self.eop_3d = [0.] * 3
      self.vel_3d = [0.] * 3
      self.angle_3d = [0.] * 3
      self.quaternion = [0.] * 4
      self.imu_gyro_3d = [0.] * 3
      self.imu_acc_3d = [0.] * 3
      self.nodes = []

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self
      buff.write(_get_struct_2B4If().pack(_x.role, _x.id, _x.stamp.secs, _x.stamp.nsecs, _x.local_time, _x.system_time, _x.voltage))
      buff.write(_get_struct_3f().pack(*self.pos_3d))
      buff.write(_get_struct_3f().pack(*self.eop_3d))
      buff.write(_get_struct_3f().pack(*self.vel_3d))
      buff.write(_get_struct_3f().pack(*self.angle_3d))
      buff.write(_get_struct_4f().pack(*self.quaternion))
      buff.write(_get_struct_3f().pack(*self.imu_gyro_3d))
      buff.write(_get_struct_3f().pack(*self.imu_acc_3d))
      length = len(self.nodes)
      buff.write(_struct_I.pack(length))
      for val1 in self.nodes:
        _x = val1
        buff.write(_get_struct_2B3f().pack(_x.role, _x.id, _x.dis, _x.fp_rssi, _x.rx_rssi))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    if python3:
      codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      if self.stamp is None:
        self.stamp = genpy.Time()
      if self.nodes is None:
        self.nodes = None
      end = 0
      _x = self
      start = end
      end += 22
      (_x.role, _x.id, _x.stamp.secs, _x.stamp.nsecs, _x.local_time, _x.system_time, _x.voltage,) = _get_struct_2B4If().unpack(str[start:end])
      start = end
      end += 12
      self.pos_3d = _get_struct_3f().unpack(str[start:end])
      start = end
      end += 12
      self.eop_3d = _get_struct_3f().unpack(str[start:end])
      start = end
      end += 12
      self.vel_3d = _get_struct_3f().unpack(str[start:end])
      start = end
      end += 12
      self.angle_3d = _get_struct_3f().unpack(str[start:end])
      start = end
      end += 16
      self.quaternion = _get_struct_4f().unpack(str[start:end])
      start = end
      end += 12
      self.imu_gyro_3d = _get_struct_3f().unpack(str[start:end])
      start = end
      end += 12
      self.imu_acc_3d = _get_struct_3f().unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.nodes = []
      for i in range(0, length):
        val1 = data_package.msg.LinktrackNode2()
        _x = val1
        start = end
        end += 14
        (_x.role, _x.id, _x.dis, _x.fp_rssi, _x.rx_rssi,) = _get_struct_2B3f().unpack(str[start:end])
        self.nodes.append(val1)
      self.stamp.canon()
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self
      buff.write(_get_struct_2B4If().pack(_x.role, _x.id, _x.stamp.secs, _x.stamp.nsecs, _x.local_time, _x.system_time, _x.voltage))
      buff.write(self.pos_3d.tostring())
      buff.write(self.eop_3d.tostring())
      buff.write(self.vel_3d.tostring())
      buff.write(self.angle_3d.tostring())
      buff.write(self.quaternion.tostring())
      buff.write(self.imu_gyro_3d.tostring())
      buff.write(self.imu_acc_3d.tostring())
      length = len(self.nodes)
      buff.write(_struct_I.pack(length))
      for val1 in self.nodes:
        _x = val1
        buff.write(_get_struct_2B3f().pack(_x.role, _x.id, _x.dis, _x.fp_rssi, _x.rx_rssi))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    if python3:
      codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      if self.stamp is None:
        self.stamp = genpy.Time()
      if self.nodes is None:
        self.nodes = None
      end = 0
      _x = self
      start = end
      end += 22
      (_x.role, _x.id, _x.stamp.secs, _x.stamp.nsecs, _x.local_time, _x.system_time, _x.voltage,) = _get_struct_2B4If().unpack(str[start:end])
      start = end
      end += 12
      self.pos_3d = numpy.frombuffer(str[start:end], dtype=numpy.float32, count=3)
      start = end
      end += 12
      self.eop_3d = numpy.frombuffer(str[start:end], dtype=numpy.float32, count=3)
      start = end
      end += 12
      self.vel_3d = numpy.frombuffer(str[start:end], dtype=numpy.float32, count=3)
      start = end
      end += 12
      self.angle_3d = numpy.frombuffer(str[start:end], dtype=numpy.float32, count=3)
      start = end
      end += 16
      self.quaternion = numpy.frombuffer(str[start:end], dtype=numpy.float32, count=4)
      start = end
      end += 12
      self.imu_gyro_3d = numpy.frombuffer(str[start:end], dtype=numpy.float32, count=3)
      start = end
      end += 12
      self.imu_acc_3d = numpy.frombuffer(str[start:end], dtype=numpy.float32, count=3)
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      self.nodes = []
      for i in range(0, length):
        val1 = data_package.msg.LinktrackNode2()
        _x = val1
        start = end
        end += 14
        (_x.role, _x.id, _x.dis, _x.fp_rssi, _x.rx_rssi,) = _get_struct_2B3f().unpack(str[start:end])
        self.nodes.append(val1)
      self.stamp.canon()
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_2B3f = None
def _get_struct_2B3f():
    global _struct_2B3f
    if _struct_2B3f is None:
        _struct_2B3f = struct.Struct("<2B3f")
    return _struct_2B3f
_struct_2B4If = None
def _get_struct_2B4If():
    global _struct_2B4If
    if _struct_2B4If is None:
        _struct_2B4If = struct.Struct("<2B4If")
    return _struct_2B4If
_struct_3f = None
def _get_struct_3f():
    global _struct_3f
    if _struct_3f is None:
        _struct_3f = struct.Struct("<3f")
    return _struct_3f
_struct_4f = None
def _get_struct_4f():
    global _struct_4f
    if _struct_4f is None:
        _struct_4f = struct.Struct("<4f")
    return _struct_4f
