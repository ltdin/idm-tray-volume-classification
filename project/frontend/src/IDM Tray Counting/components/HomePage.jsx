import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Autoplay, Pagination, Navigation } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';
import banners from '../data/banners';

function HomePage() {
  return (
    <div style={{ width: '100%', height: '400px' }}>
      <Swiper
        modules={[Autoplay, Pagination, Navigation]}
        autoplay={{ delay: 4000, disableOnInteraction: false }}
        pagination={{ clickable: true }}
        navigation
        loop
        style={{ height: '100%' }}
      >
        {banners.map((banner, index) => (
          <SwiperSlide key={index}>
            <div
              style={{
                backgroundImage: `url(${banner.img})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                width: '100%',
                height: '400px',
                position: 'relative'
              }}
            >
              <div style={{
                position: 'absolute',
                bottom: '20%',
                left: '10%',
                color: 'white',
                background: 'rgba(0, 0, 0, 0)',
                padding: '1rem',
                borderRadius: '8px',
                maxWidth: '50%'
              }}>
                <h1>{banner.caption}</h1>
                <p>{banner.description}</p>
              </div>
            </div>
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  );
}

export default HomePage;
