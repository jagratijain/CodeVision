import React, { useState, useRef } from "react";
import { 
  Upload as UploadIcon, 
  X, 
  Check, 
  Loader2, 
  ImagePlus, 
  Film 
} from "lucide-react";
import Navbar from "./Navbar";

const Dashboard = () => {
  const [mediaFiles, setMediaFiles] = useState({
    image: null,
    video: null
  });
  const [loading, setLoading] = useState(false);
  const imageInputRef = useRef(null);
  const videoInputRef = useRef(null);

  const handleFileUpload = (type, event) => {
    const file = event.target.files[0];
    if (file) {
      const fileType = type === 'image' ? 'image/' : 'video/';
      if (file.type.startsWith(fileType)) {
        setMediaFiles(prev => ({
          ...prev,
          [type]: {
            file,
            preview: URL.createObjectURL(file),
            type: file.type
          }
        }));
      }
    }
  };


  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!mediaFiles.image && !mediaFiles.video) {
      alert("Please upload at least one media file.");
      return;
    }

    setLoading(true);

    const uploadData = new FormData();
    if (mediaFiles.video) {
      uploadData.append("video", mediaFiles.video.file);
    }
    if (mediaFiles.image) {
      uploadData.append("mask", mediaFiles.image.file);
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/process_media", {
        method: "POST",
        body: uploadData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const result = await response.json();
      console.log("Success:", result);

      alert("Terminated!");
      setMediaFiles({ image: null, video: null });
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to process media. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const MediaUploadBox = ({ type, icon: Icon }) => {
    const file = mediaFiles[type];

    return (
      <div className="bg-white rounded-xl p-6 border-2 border-gray-700 hover:border-[#dcc7ae] transition-all group">
        <input
          type="file"
          ref={type === 'image' ? imageInputRef : videoInputRef}
          accept={`${type}/*`}
          onChange={(e) => handleFileUpload(type, e)}
          className="hidden"
          id={`${type}Upload`}
        />
        <label 
          htmlFor={`${type}Upload`} 
          className="cursor-pointer flex flex-col items-center"
        >
          {file ? (
            <div className="relative w-full">
              {type === 'image' ? (
                // <p>Image Uploaded</p>
                <img 
                  src={file.preview} 
                  alt="Preview" 
                  className="w-full h-48 object-cover rounded-lg"
                />
              ) : (
                // <p>Video Uploaded</p>
                <video
                  src={file.preview}
                  className="w-full h-48 object-cover rounded-lg"
                  controls
                />
              )}
              
            </div>
          ) : (
            <div className="flex flex-col items-center">
              <Icon 
                className="text-gray-500 group-hover:text-[#dcc7ae] transition-colors" 
                size={48} 
              />
              <p className="mt-3 text-sm text-gray-400 group-hover:text-[#dcc7ae]">
                Upload {type === 'image' ? 'Image' : 'Video'}
              </p>
            </div>
          )}
        </label>
      </div>
    );
  };

  return (
    <>
      <Navbar />
      
      <div className="bg-gradient-to-br from-[#FFEFDB] via-[#FFDDC1] to-[#F7F4E1] min-h-screen flex items-center justify-center px-4 py-12">

      <div className="w-full max-w-4xl rounded-3xl shadow-2xl p-10">

          
          
          <form onSubmit={handleSubmit} className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <MediaUploadBox type="image" icon={ImagePlus} />
              <MediaUploadBox type="video" icon={Film} />
            </div>

            <div className="text-center">
              <button
                type="submit"
                disabled={!mediaFiles.image || !mediaFiles.video || loading}
                className="bg-[#a0835e] text-white px-10 py-4 rounded-xl 
                hover:bg-[#9c723f] transition-colors 
                flex items-center justify-center mx-auto 
                disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <Loader2 className="animate-spin mr-3" size={24} />
                ) : (
                  <Check  className="mr-3" size={24} />
                )}
                {loading ? "Processing..." : "Run"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default Dashboard;