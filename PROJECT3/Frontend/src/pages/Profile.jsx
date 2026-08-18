import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { FiPlus, FiTrash2, FiUser, FiArrowLeft } from 'react-icons/fi';
import Layout from '../components/common/Layout';
import Loader from '../components/common/Loader';
import { userService } from '../services/apiService';
import { LANGUAGES, CROP_TYPES } from '../utils/constants';
import { formatDate } from '../utils/helpers';
import { translateCropName } from '../utils/translationHelpers';

const Profile = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [crops, setCrops] = useState([]);
  const [showAddCrop, setShowAddCrop] = useState(false);
  const [editingProfile, setEditingProfile] = useState(false);

  const [profileForm, setProfileForm] = useState({
    email: '',
    phone: '',
    language: 'en',
    location_lat: null,
    location_lon: null,
  });

  const [cropForm, setCropForm] = useState({
    crop_type: 'tomato',
    variety: '',
    area_size: '',
    location: '',
  });

  useEffect(() => {
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    try {
      const [profileData, cropsData] = await Promise.all([
        userService.getProfile(),
        userService.getCrops(),
      ]);

      const profile = profileData.data || {};
      setProfile(profile);
      setProfileForm({
        email: profile.email || '',
        phone: profile.phone || '',
        language: profile.language || 'en',
        location_lat: profile.location_lat || null,
        location_lon: profile.location_lon || null,
      });
      setCrops(cropsData.data || []);
    } catch (error) {
      toast.error('Failed to fetch profile data');
    } finally {
      setLoading(false);
    }
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    try {
      const updated = await userService.updateProfile(profileForm);
      setProfile(updated);
      setEditingProfile(false);
      toast.success('Profile updated successfully');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to update profile');
    }
  };

  const handleAddCrop = async (e) => {
    e.preventDefault();
    try {
      const newCrop = await userService.addCrop({
        ...cropForm,
        area_size: parseFloat(cropForm.area_size) || null,
      });
      setCrops([...crops, newCrop]);
      setShowAddCrop(false);
      setCropForm({
        crop_type: 'tomato',
        variety: '',
        area_size: '',
        location: '',
      });
      toast.success('Crop added successfully');
    } catch (error) {
      toast.error('Failed to add crop');
    }
  };

  const handleDeleteCrop = async (cropId) => {
    if (!window.confirm('Are you sure you want to delete this crop?')) return;

    try {
      await userService.deleteCrop(cropId);
      setCrops(crops.filter((crop) => crop.id !== cropId));
      toast.success('Crop deleted successfully');
    } catch (error) {
      toast.error('Failed to delete crop');
    }
  };

  if (loading) {
    return (
      <Layout>
        <Loader />
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-6 max-w-4xl mx-auto">
        {/* Back Button */}
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors group"
        >
          <FiArrowLeft className="group-hover:-translate-x-1 transition-transform" />
          <span className="font-medium">{t('back_to_dashboard')}</span>
        </button>

        <h1 className="text-3xl font-bold">{t('profile')}</h1>

        {/* Profile Information */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="bg-primary-100 text-primary-600 w-16 h-16 rounded-full flex items-center justify-center text-2xl">
                <FiUser />
              </div>
              <div>
                <h2 className="text-2xl font-semibold">{profile?.username}</h2>
                <p className="text-gray-600">{profile?.email}</p>
              </div>
            </div>
            <button
              onClick={() => setEditingProfile(!editingProfile)}
              className="btn-secondary"
            >
              {editingProfile ? t('cancel') : t('edit_profile')}
            </button>
          </div>

          {editingProfile ? (
            <form onSubmit={handleProfileUpdate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('email')}
                </label>
                <input
                  type="email"
                  value={profileForm.email}
                  onChange={(e) => setProfileForm({ ...profileForm, email: e.target.value })}
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('phone')}
                </label>
                <input
                  type="tel"
                  value={profileForm.phone}
                  onChange={(e) => setProfileForm({ ...profileForm, phone: e.target.value })}
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('language')}
                </label>
                <select
                  value={profileForm.language}
                  onChange={(e) => setProfileForm({ ...profileForm, language: e.target.value })}
                  className="input-field"
                >
                  {LANGUAGES.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.nativeName}
                    </option>
                  ))}
                </select>
              </div>

              <button type="submit" className="btn-primary">
                {t('save_changes')}
              </button>
            </form>
          ) : (
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">{t('phone')}:</span>{' '}
                <span className="font-semibold">{profile?.phone || t('not_provided')}</span>
              </div>
              <div>
                <span className="text-gray-600">{t('language')}:</span>{' '}
                <span className="font-semibold">
                  {LANGUAGES.find((l) => l.code === profile?.language)?.nativeName}
                </span>
              </div>
              <div>
                <span className="text-gray-600">{t('member_since')}</span>{' '}
                <span className="font-semibold">{formatDate(profile?.created_at)}</span>
              </div>
            </div>
          )}
        </div>

        {/* My Crops */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-semibold">{t('my_crops')}</h2>
            <button
              onClick={() => setShowAddCrop(!showAddCrop)}
              className="btn-primary flex items-center space-x-2"
            >
              <FiPlus />
              <span>{t('add_crop')}</span>
            </button>
          </div>

          {/* Add Crop Form */}
          {showAddCrop && (
            <form onSubmit={handleAddCrop} className="mb-6 p-4 bg-gray-50 rounded-lg">
              <h3 className="font-semibold mb-3">{t('add_new_crop')}</h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('crop_type')}
                  </label>
                  <select
                    value={cropForm.crop_type}
                    onChange={(e) => setCropForm({ ...cropForm, crop_type: e.target.value })}
                    className="input-field"
                  >
                    {CROP_TYPES.map((crop) => (
                      <option key={crop} value={crop}>
                        {translateCropName(crop, t)}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('variety')}
                  </label>
                  <input
                    type="text"
                    value={cropForm.variety}
                    onChange={(e) => setCropForm({ ...cropForm, variety: e.target.value })}
                    className="input-field"
                    placeholder="e.g., Roma, Russet"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Area Size (acres)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={cropForm.area_size}
                    onChange={(e) => setCropForm({ ...cropForm, area_size: e.target.value })}
                    className="input-field"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('location')}
                  </label>
                  <input
                    type="text"
                    value={cropForm.location}
                    onChange={(e) => setCropForm({ ...cropForm, location: e.target.value })}
                    className="input-field"
                    placeholder="e.g., Farm Area 1"
                  />
                </div>
              </div>

              <div className="flex space-x-3 mt-4">
                <button type="submit" className="btn-primary">
                  Add Crop
                </button>
                <button
                  type="button"
                  onClick={() => setShowAddCrop(false)}
                  className="btn-secondary"
                >
                  {t('cancel')}
                </button>
              </div>
            </form>
          )}

          {/* Crops List */}
          {crops.length === 0 ? (
            <p className="text-gray-600 text-center py-8">
              {t('no_crops_message')}
            </p>
          ) : (
            <div className="grid md:grid-cols-2 gap-4">
              {crops.map((crop) => (
                <div key={crop.id} className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="flex items-start justify-between">
                    <div className="flex-grow">
                      <h3 className="font-semibold text-lg">{translateCropName(crop.crop_type, t)}</h3>
                      {crop.variety && (
                        <p className="text-sm text-gray-600">{t('variety')}: {crop.variety}</p>
                      )}
                      {crop.area_size && (
                        <p className="text-sm text-gray-600">{t('area')}: {crop.area_size} {t('acres')}</p>
                      )}
                      {crop.location && (
                        <p className="text-sm text-gray-600">{t('location')}: {crop.location}</p>
                      )}
                      {crop.planted_date && (
                        <p className="text-xs text-gray-500 mt-2">
                          {t('planted')}: {formatDate(crop.planted_date)}
                        </p>
                      )}
                    </div>
                    <button
                      onClick={() => handleDeleteCrop(crop.id)}
                      className="text-red-600 hover:text-red-800"
                    >
                      <FiTrash2 />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default Profile;
