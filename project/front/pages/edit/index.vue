<script setup>
import { ref, onMounted } from 'vue'

const activeTab = ref('brandClient')

// 데이터 상태
const brandClients = ref([])
const projects = ref([])
const works = ref([])
const mainCategories = ref([])
const subCategories = ref([])
const inquiries = ref([])
const siteSetting = ref({ 
  logo_kr: '', 
  logo_en: '', 
  about_headings: [
    { text: '브랜드의 고도를 높이는', is_highlighted: false },
    { text: '우상향 프로덕션', is_highlighted: false }
  ],
  email: '',
  phone: '',
  address: '',
  instagram_handle: '',
  instagram_url: '',
  contact_title: '',
  footer_slogan_main: ["당신의 브랜드,", "한 단계 더 위로"],
  footer_slogan_sub: '',
  is_service_visible: true,
  service_title: 'MONTHLY PLAN',
  service_desc: '영상 운영 가격 / 한달 기준',
  is_about_visible: true,
  about_title: 'ABOUT THE STUDIO',
  about_desc: '하이어, 더 높은 곳으로',
  is_contact_visible: true,
  contact_header_title: 'GET IN TOUCH',
  contact_header_desc: '하이어, 더 높은 곳으로'
})

// 폼 상태
const formBc = ref({ name: '', subtitle: '' })
const formProject = ref({ title: '', subtitle: '', client: '' })
const formMainCategory = ref({ name: '', order: 0 })
const formSubCategory = ref({ name: '', main_category: '', order: 0, is_vertical: false, is_instagram: false })
const formWork = ref({ 
  title: '', 
  sub_category: '', 
  youtube_link: '', 
  instagram_embed: '',
  content: '',
  status: 'COMPLETED', 
  is_visible: true,
  thumbnail_url: '' // 유튜브 썸네일 미리보기용
})

const selectedPlatform = ref('YOUTUBE') // 'YOUTUBE' 또는 'INSTAGRAM'

// 카테고리 인라인 수정 상태
const editingMainCategoryId = ref(null)
const editingMainCategoryData = ref({ id: null, name: '', order: 0 })

const editingSubCategoryId = ref(null)
const editingSubCategoryData = ref({ id: null, name: '', main_category: '', order: 0, is_vertical: false, is_instagram: false })

// 브랜드 클라이언트 인라인 수정 상태
const editingBrandClientId = ref(null)
const editingBrandClientData = ref({ id: null, name: '', subtitle: '' })

// 프로젝트 인라인 수정 상태
const editingProjectId = ref(null)
const editingProjectData = ref({ id: null, title: '', subtitle: '', client: '' })

// 유튜브 검색 상태
const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)

// 비디오 플레이어 상태
const playingVideoId = ref('')

// 플랜(요금제) 관련 상태
const plans = ref([])
const planTypes = ref([])
const recommends = ref([])
const operations = ref([])
const productions = ref([])
const items = ref([])

const formRecommend = ref({ name: '' })
const formPlanType = ref({ name: '' })
const formOperation = ref({ name: '' })
const formProduction = ref({ name: '' })
const formItem = ref({ name: '' })
const formPlan = ref({ 
  plan_type: null, name: '', subname: '', price: 0, 
  recommend_ids: [], operation_ids: [], production_ids: [], item_ids: [] 
})

// 플랜 관련 데이터 불러오기
const loadPlans = async () => {
  try { plans.value = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/product/plans/') } catch (e) { console.error(e) }
}
const loadPlanTypes = async () => {
  try { planTypes.value = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/product/plan_types/') } catch (e) { console.error(e) }
}
const loadRecommends = async () => {
  try { recommends.value = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/product/recommends/') } catch (e) { console.error(e) }
}
const loadOperations = async () => {
  try { operations.value = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/product/operations/') } catch (e) { console.error(e) }
}
const loadProductions = async () => {
  try { productions.value = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/product/productions/') } catch (e) { console.error(e) }
}
const loadItems = async () => {
  try { items.value = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/product/items/') } catch (e) { console.error(e) }
}

const addSimpleItem = async (endpoint, formData, reloadFunc) => {
  if (!formData.name) return alert('항목 이름을 입력해주세요.')
  try {
    await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/product/${endpoint}/`, { method: 'POST', body: { name: formData.name } })
    formData.name = ''
    reloadFunc()
  } catch (e) { console.error(e); alert('추가 실패') }
}
const deleteSimpleItem = async (endpoint, id, reloadFunc) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  try {
    await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/product/${endpoint}/${id}/`, { method: 'DELETE' })
    reloadFunc()
  } catch (e) { console.error(e); alert('삭제 실패') }
}

const addPlan = async () => {
  if (!formPlan.value.name || formPlan.value.price === null) return alert('플랜명과 가격을 입력해주세요.')
  try {
    await $fetch(useRuntimeConfig().public.apiBaseUrl + '/product/plans/', {
      method: 'POST',
      body: formPlan.value
    })
    formPlan.value = { plan_type: null, name: '', subname: '', price: 0, recommend_ids: [], operation_ids: [], production_ids: [], item_ids: [] }
    alert('요금제가 추가되었습니다.')
    loadPlans()
  } catch (e) { console.error(e); alert('추가 실패') }
}
const deletePlan = async (id) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  try {
    await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/product/plans/${id}/`, { method: 'DELETE' })
    loadPlans()
  } catch (e) { console.error(e); alert('삭제 실패') }
}

// 데이터 불러오기 함수
const loadBrandClients = async () => {
  try {
    brandClients.value = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/admin/brandclients/')
  } catch (e) { console.error(e) }
}
const loadProjects = async () => {
  try {
    projects.value = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/admin/projects/')
  } catch (e) { console.error(e) }
}
const loadWorks = async () => {
  try {
    works.value = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/admin/works/')
  } catch (e) { console.error(e) }
}
const loadMainCategories = async () => {
  try {
    mainCategories.value = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/admin/main-categories/')
  } catch (e) { console.error(e) }
}
const loadSubCategories = async () => {
  try {
    subCategories.value = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/admin/sub-categories/')
  } catch (e) { console.error(e) }
}
const loadInquiries = async () => {
  try {
    inquiries.value = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/inquiries/')
  } catch (e) { console.error(e) }
}
const loadSiteSetting = async () => {
  try {
    const data = await $fetch(useRuntimeConfig().public.apiBaseUrl + '/system/settings/')
    let headings = data.about_headings
    if (!headings || headings.length === 0) {
      headings = [
        { text: '브랜드의 고도를 높이는', is_highlighted: false },
        { text: '우상향 프로덕션', is_highlighted: false }
      ]
    }
    siteSetting.value = { 
      logo_kr: data.logo_kr || '', 
      logo_en: data.logo_en || '',
      about_headings: headings,
      email: data.email || 'higher3pd@gmail.com',
      phone: data.phone || '+82 10-3313-0388',
      address: data.address || '경기도 의정부시, KR',
      instagram_handle: data.instagram_handle || '@higher.production',
      instagram_url: data.instagram_url || 'https://instagram.com/higher.production',
      contact_title: data.contact_title || "LET'S GO HIGHER",
      footer_slogan_main: Array.isArray(data.footer_slogan_main) ? data.footer_slogan_main : ["당신의 브랜드,", "한 단계 더 위로"],
      footer_slogan_sub: data.footer_slogan_sub || "Let's go higher.",
      is_service_visible: data.is_service_visible ?? true,
      service_title: data.service_title || 'MONTHLY PLAN',
      service_desc: data.service_desc || '영상 운영 가격 / 한달 기준',
      is_about_visible: data.is_about_visible ?? true,
      about_title: data.about_title || 'ABOUT THE STUDIO',
      about_desc: data.about_desc || '하이어, 더 높은 곳으로',
      is_contact_visible: data.is_contact_visible ?? true,
      contact_header_title: data.contact_header_title || 'GET IN TOUCH',
      contact_header_desc: data.contact_header_desc || '하이어, 더 높은 곳으로'
    }
  } catch (e) { console.error(e) }
}

const addAboutHeading = () => {
  siteSetting.value.about_headings.push({ text: '', is_highlighted: false })
}

const removeAboutHeading = (index) => {
  if (siteSetting.value.about_headings.length > 1) {
    siteSetting.value.about_headings.splice(index, 1)
  } else {
    alert('최소 한 줄은 필요합니다.')
  }
}

onMounted(() => {
  loadBrandClients()
  loadProjects()
  loadWorks()
  loadMainCategories()
  loadSubCategories()
  loadInquiries()
  loadSiteSetting()
  loadPlanTypes()
  loadPlans()
  loadRecommends()
  loadOperations()
  loadProductions()
  loadItems()
})

// 추가 함수들
const addBrandClient = async () => {
  if (!formBc.value.name) return alert('브랜드명을 입력해주세요.')
  try {
    await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/admin/brandclients/', {
      method: 'POST',
      body: { 
        name: formBc.value.name,
        subtitle: formBc.value.subtitle || ''
      }
    })
    formBc.value = { name: '', subtitle: '' }
    alert('브랜드 클라이언트가 추가되었습니다.')
    loadBrandClients()
  } catch (e) {
    console.error(e)
    alert('추가 실패')
  }
}

const deleteBrandClient = async (id) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/brandclients/${id}/`, { method: 'DELETE' })
  loadBrandClients()
}

const startEditingBrandClient = (bc) => {
  editingBrandClientId.value = bc.id
  editingBrandClientData.value = { 
    id: bc.id, 
    name: bc.name, 
    subtitle: bc.subtitle 
  }
}

const cancelEditingBrandClient = () => {
  editingBrandClientId.value = null
}

const saveBrandClient = async () => {
  try {
    await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/brandclients/${editingBrandClientData.value.id}/`, {
      method: 'PATCH',
      body: { 
        name: editingBrandClientData.value.name,
        subtitle: editingBrandClientData.value.subtitle || ''
      }
    })
    alert('브랜드가 성공적으로 수정되었습니다.')
    editingBrandClientId.value = null
    loadBrandClients()
  } catch (e) {
    console.error(e)
    alert('브랜드 수정에 실패했습니다.')
    loadBrandClients()
  }
}

// 대분류 관리
const addMainCategory = async () => {
  if (!formMainCategory.value.name) return alert('대분류명을 입력해주세요.')
  try {
    await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/admin/main-categories/', {
      method: 'POST',
      body: { name: formMainCategory.value.name, order: formMainCategory.value.order || 0 }
    })
    formMainCategory.value = { name: '', order: 0 }
    alert('대분류가 추가되었습니다.')
    loadMainCategories()
  } catch (e) { console.error(e); alert('추가 실패') }
}
const startEditingMainCategory = (cat) => {
  editingMainCategoryId.value = cat.id
  editingMainCategoryData.value = { id: cat.id, name: cat.name, order: cat.order }
}
const cancelEditingMainCategory = () => {
  editingMainCategoryId.value = null
}
const saveMainCategory = async () => {
  try {
    await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/main-categories/${editingMainCategoryData.value.id}/`, {
      method: 'PATCH',
      body: { name: editingMainCategoryData.value.name, order: editingMainCategoryData.value.order }
    })
    editingMainCategoryId.value = null
    loadMainCategories()
  } catch (e) { console.error(e); alert('수정 실패') }
}
const deleteMainCategory = async (id) => {
  if (!confirm('대분류를 삭제하면 하위 중분류도 삭제될 수 있습니다. 진행할까요?')) return
  await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/main-categories/${id}/`, { method: 'DELETE' })
  loadMainCategories()
  loadSubCategories()
}

// 중분류 관리
const addSubCategory = async () => {
  if (!formSubCategory.value.name || !formSubCategory.value.main_category) return alert('대분류와 중분류명을 모두 입력/선택해주세요.')
  try {
    await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/admin/sub-categories/', {
      method: 'POST',
      body: { 
        name: formSubCategory.value.name,
        main_category: formSubCategory.value.main_category,
        order: formSubCategory.value.order || 0,
        is_vertical: formSubCategory.value.is_vertical || false,
        is_instagram: formSubCategory.value.is_instagram || false
      }
    })
    formSubCategory.value = { name: '', main_category: '', order: 0, is_vertical: false, is_instagram: false }
    alert('중분류가 추가되었습니다.')
    loadSubCategories()
  } catch (e) { console.error(e); alert('추가 실패') }
}
const startEditingSubCategory = (cat) => {
  editingSubCategoryId.value = cat.id
  editingSubCategoryData.value = { 
    id: cat.id, 
    name: cat.name, 
    main_category: cat.main_category,
    order: cat.order, 
    is_vertical: cat.is_vertical,
    is_instagram: cat.is_instagram
  }
}
const cancelEditingSubCategory = () => {
  editingSubCategoryId.value = null
}
const saveSubCategory = async () => {
  try {
    await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/sub-categories/${editingSubCategoryData.value.id}/`, {
      method: 'PATCH',
      body: { 
        name: editingSubCategoryData.value.name,
        main_category: editingSubCategoryData.value.main_category,
        order: editingSubCategoryData.value.order,
        is_vertical: editingSubCategoryData.value.is_vertical,
        is_instagram: editingSubCategoryData.value.is_instagram
      }
    })
    editingSubCategoryId.value = null
    loadSubCategories()
  } catch (e) { console.error(e); alert('수정 실패') }
}
const deleteSubCategory = async (id) => {
  if (!confirm('정말 삭제하시겠습니까? 관련된 영상이 안 보일 수 있습니다.')) return
  await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/sub-categories/${id}/`, { method: 'DELETE' })
  loadSubCategories()
}

const addProject = async () => {
  if (!formProject.value.title) return alert('프로젝트명을 입력해주세요.')
  try {
    await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/admin/projects/', {
      method: 'POST',
      body: { 
        title: formProject.value.title,
        subtitle: formProject.value.subtitle || '',
        client: formProject.value.client || null 
      }
    })
    formProject.value = { title: '', subtitle: '', client: '' }
    alert('납품 프로젝트가 추가되었습니다.')
    loadProjects()
  } catch (e) {
    console.error(e)
    alert('추가 실패')
  }
}

const deleteProject = async (id) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/projects/${id}/`, { method: 'DELETE' })
  loadProjects()
}

const startEditingProject = (p) => {
  editingProjectId.value = p.id
  editingProjectData.value = { 
    id: p.id, 
    title: p.title, 
    subtitle: p.subtitle,
    client: p.client 
  }
}

const cancelEditingProject = () => {
  editingProjectId.value = null
}

const saveProject = async () => {
  try {
    await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/projects/${editingProjectData.value.id}/`, {
      method: 'PATCH',
      body: { 
        title: editingProjectData.value.title,
        subtitle: editingProjectData.value.subtitle || '',
        client: editingProjectData.value.client || null
      }
    })
    alert('프로젝트가 성공적으로 수정되었습니다.')
    editingProjectId.value = null
    loadProjects()
  } catch (e) {
    console.error(e)
    alert('프로젝트 수정에 실패했습니다.')
    loadProjects()
  }
}

// 유튜브 정보 불러오기 API 연동
const fetchYoutubeInfo = async () => {
  if (!formWork.value.youtube_link) {
    return alert('유튜브 링크를 먼저 입력해주세요.')
  }
  try {
    const data = await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/youtube-info/?url=${encodeURIComponent(formWork.value.youtube_link)}`)
    if (data.title) {
      formWork.value.title = data.title
      formWork.value.thumbnail_url = data.thumbnail_url
      alert('유튜브 정보를 성공적으로 불러왔습니다.')
    }
  } catch (e) {
    console.error(e)
    alert('유튜브 정보를 불러오는데 실패했습니다. 올바른 링크인지 확인해주세요.')
  }
}

const searchYoutube = async () => {
  if (!searchQuery.value) return alert('검색어를 입력해주세요.')
  isSearching.value = true
  searchResults.value = []
  
  try {
    const data = await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/youtube-search/?q=${encodeURIComponent(searchQuery.value)}`)
    if (data.error) {
      alert(data.error)
    } else {
      searchResults.value = data
      if (data.length === 0) alert('검색 결과가 없습니다.')
    }
  } catch (e) {
    console.error(e)
    alert(e.response?._data?.error || '검색에 실패했습니다.')
  } finally {
    isSearching.value = false
  }
}

const selectYoutubeResult = (result) => {
  formWork.value.title = result.title
  formWork.value.youtube_link = result.youtube_link
  formWork.value.thumbnail_url = result.thumbnail_url
  searchResults.value = [] // 선택 후 목록 닫기
  searchQuery.value = ''
}

// 최종 영상(Work) 추가
const addWork = async () => {
  if (!formWork.value.title) return alert('작품명(제목)을 입력해주세요. (유튜브 정보 불러오기를 추천합니다)')
  if (!formWork.value.sub_category) return alert('카테고리(중분류)를 선택해주세요.')
  
  try {
    await $fetch(useRuntimeConfig().public.apiBaseUrl + '/work/admin/works/', {
      method: 'POST',
      body: { 
        title: formWork.value.title,
        youtube_link: formWork.value.youtube_link || null,
        instagram_embed: formWork.value.instagram_embed || null,
        sub_category: formWork.value.sub_category,
        content: formWork.value.content || '',
        status: formWork.value.status,
        is_visible: formWork.value.is_visible
      }
    })
    // 초기화
    formWork.value = { title: '', sub_category: '', youtube_link: '', instagram_embed: '', content: '', status: 'COMPLETED', is_visible: true, thumbnail_url: '' }
    alert('최종 영상이 성공적으로 추가되었습니다.')
    loadWorks()
  } catch (e) {
    console.error(e)
    alert('추가 실패')
  }
}

const deleteWork = async (id) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/works/${id}/`, { method: 'DELETE' })
  loadWorks()
}

// 영상 상태/공개여부 실시간 수정
const updateWorkStatus = async (work) => {
  try {
    await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/works/${work.id}/`, {
      method: 'PATCH',
      body: { status: work.status }
    })
  } catch (e) {
    console.error(e)
    alert('상태 업데이트에 실패했습니다.')
    loadWorks()
  }
}

const updateWorkVisibility = async (work) => {
  try {
    await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/admin/works/${work.id}/`, {
      method: 'PATCH',
      body: { is_visible: work.is_visible }
    })
  } catch (e) {
    console.error(e)
    alert('공개 여부 업데이트에 실패했습니다.')
    loadWorks()
  }
}

// 영상 바로 시청하기 (모달 띄우기)
const playVideo = (url) => {
  if (!url) return
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/
  const match = url.match(regExp)
  if (match && match[2].length === 11) {
    playingVideoId.value = match[2]
  } else {
    window.open(url, '_blank') // 파싱 실패시 새창으로 열기
  }
}

const closeVideo = () => {
  playingVideoId.value = ''
}

// 문의 내역 삭제
const deleteInquiry = async (id) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/inquiries/${id}/`, { method: 'DELETE' })
  loadInquiries()
}

// 문의 읽음 처리
const toggleInquiryRead = async (inq) => {
  try {
    await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/inquiries/${inq.id}/`, {
      method: 'PATCH',
      body: { is_read: !inq.is_read }
    })
    loadInquiries()
  } catch (e) {
    console.error(e)
  }
}

// 문의 상태 변경 (미접수, 처리 중, 처리 완료)
const updateInquiryStatus = async (inq) => {
  try {
    await $fetch(`${useRuntimeConfig().public.apiBaseUrl}/work/inquiries/${inq.id}/`, {
      method: 'PATCH',
      body: { status: inq.status }
    })
  } catch (e) {
    console.error(e)
    alert('상태 업데이트에 실패했습니다.')
    loadInquiries()
  }
}

// 사이트 설정 저장
const saveSiteSetting = async () => {
  try {
    await $fetch(useRuntimeConfig().public.apiBaseUrl + '/system/settings/', {
      method: 'PATCH',
      body: siteSetting.value
    })
    alert('사이트 설정이 성공적으로 저장되었습니다.')
  } catch (e) {
    console.error(e)
    alert('사이트 설정 저장에 실패했습니다.')
  }
}
</script>

<template>
  <div class="profile-layout edit-layout">
    <div class="profile-grid">
      <!-- 사이드바 -->
      <aside class="dashboard-panel">
        <h2 class="panel-title">데이터 관리</h2>
        <ul class="admin-menu">
          <li :class="{ active: activeTab === 'brandClient' }" @click="activeTab = 'brandClient'">브랜드 클라이언트</li>
          <li :class="{ active: activeTab === 'project' }" @click="activeTab = 'project'">납품 프로젝트</li>
          <li :class="{ active: activeTab === 'category' }" @click="activeTab = 'category'">카테고리 관리</li>
          <li :class="{ active: activeTab === 'work' }" @click="activeTab = 'work'">최종 영상 (Works)</li>
          <li :class="{ active: activeTab === 'inquiry' }" @click="activeTab = 'inquiry'">문의 내역 관리</li>
          <li :class="{ active: activeTab === 'plan' }" @click="activeTab = 'plan'">플랜(요금제) 관리</li>
          <li :class="{ active: activeTab === 'siteSetting' }" @click="activeTab = 'siteSetting'">사이트 설정</li>
        </ul>
      </aside>

      <!-- 메인 폼 영역 -->
      <main class="profile-panel">
        
        <!-- 플랜(요금제) 관리 탭 -->
        <div v-if="activeTab === 'plan'">
          <h2 class="panel-title">플랜(요금제) 관리</h2>
          
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 40px;">
            <!-- 플랜 종류 -->
            <div class="section" style="margin-bottom: 0;">
              <h3>플랜 종류 관리</h3>
              <div class="form-row" style="margin-bottom: 10px;">
                <input v-model="formPlanType.name" type="text" placeholder="예: BASIC, GROWTH" class="flex-1" />
                <button class="btn-submit" @click="addSimpleItem('plan_types', formPlanType, loadPlanTypes)">추가</button>
              </div>
              <ul style="list-style:none; padding:0; margin:0; border:1px solid #eee; border-radius:4px; max-height:150px; overflow-y:auto;">
                <li v-for="item in planTypes" :key="item.id" style="display:flex; justify-content:space-between; padding:8px 10px; border-bottom:1px solid #eee; font-size:13px;">
                  <span>{{ item.name }}</span>
                  <button class="btn-delete" @click="deleteSimpleItem('plan_types', item.id, loadPlanTypes)" style="padding:2px 6px;">삭제</button>
                </li>
              </ul>
            </div>

            <!-- 추천 대상 -->
            <div class="section" style="margin-bottom: 0;">
              <h3>추천 대상 관리</h3>
              <div class="form-row" style="margin-bottom: 10px;">
                <input v-model="formRecommend.name" type="text" placeholder="항목 이름" class="flex-1" />
                <button class="btn-submit" @click="addSimpleItem('recommends', formRecommend, loadRecommends)">추가</button>
              </div>
              <ul style="list-style:none; padding:0; margin:0; border:1px solid #eee; border-radius:4px; max-height:150px; overflow-y:auto;">
                <li v-for="item in recommends" :key="item.id" style="display:flex; justify-content:space-between; padding:8px 10px; border-bottom:1px solid #eee; font-size:13px;">
                  <span>{{ item.name }}</span>
                  <button class="btn-delete" @click="deleteSimpleItem('recommends', item.id, loadRecommends)" style="padding:2px 6px;">삭제</button>
                </li>
              </ul>
            </div>
            
            <!-- 운영 목적 -->
            <div class="section" style="margin-bottom: 0;">
              <h3>운영 목적 관리</h3>
              <div class="form-row" style="margin-bottom: 10px;">
                <input v-model="formOperation.name" type="text" placeholder="항목 이름" class="flex-1" />
                <button class="btn-submit" @click="addSimpleItem('operations', formOperation, loadOperations)">추가</button>
              </div>
              <ul style="list-style:none; padding:0; margin:0; border:1px solid #eee; border-radius:4px; max-height:150px; overflow-y:auto;">
                <li v-for="item in operations" :key="item.id" style="display:flex; justify-content:space-between; padding:8px 10px; border-bottom:1px solid #eee; font-size:13px;">
                  <span>{{ item.name }}</span>
                  <button class="btn-delete" @click="deleteSimpleItem('operations', item.id, loadOperations)" style="padding:2px 6px;">삭제</button>
                </li>
              </ul>
            </div>

            <!-- 촬영 / 편수 -->
            <div class="section" style="margin-bottom: 0;">
              <h3>촬영 / 편수 관리</h3>
              <div class="form-row" style="margin-bottom: 10px;">
                <input v-model="formProduction.name" type="text" placeholder="항목 이름" class="flex-1" />
                <button class="btn-submit" @click="addSimpleItem('productions', formProduction, loadProductions)">추가</button>
              </div>
              <ul style="list-style:none; padding:0; margin:0; border:1px solid #eee; border-radius:4px; max-height:150px; overflow-y:auto;">
                <li v-for="item in productions" :key="item.id" style="display:flex; justify-content:space-between; padding:8px 10px; border-bottom:1px solid #eee; font-size:13px;">
                  <span>{{ item.name }}</span>
                  <button class="btn-delete" @click="deleteSimpleItem('productions', item.id, loadProductions)" style="padding:2px 6px;">삭제</button>
                </li>
              </ul>
            </div>

            <!-- 제작 항목 -->
            <div class="section" style="margin-bottom: 0;">
              <h3>제작 항목 관리</h3>
              <div class="form-row" style="margin-bottom: 10px;">
                <input v-model="formItem.name" type="text" placeholder="항목 이름" class="flex-1" />
                <button class="btn-submit" @click="addSimpleItem('items', formItem, loadItems)">추가</button>
              </div>
              <ul style="list-style:none; padding:0; margin:0; border:1px solid #eee; border-radius:4px; max-height:150px; overflow-y:auto;">
                <li v-for="item in items" :key="item.id" style="display:flex; justify-content:space-between; padding:8px 10px; border-bottom:1px solid #eee; font-size:13px;">
                  <span>{{ item.name }}</span>
                  <button class="btn-delete" @click="deleteSimpleItem('items', item.id, loadItems)" style="padding:2px 6px;">삭제</button>
                </li>
              </ul>
            </div>
          </div>

          <hr style="border:none; border-top:1px solid #eee; margin:40px 0;">

          <div class="section">
            <h3>새 요금제(Plan) 추가</h3>
            <div class="form-row" style="margin-bottom:15px;">
              <div class="form-group flex-1">
                <label>플랜 종류</label>
                <select v-model="formPlan.plan_type">
                  <option :value="null">플랜 종류 선택</option>
                  <option v-for="pt in planTypes" :key="pt.id" :value="pt.id">{{ pt.name }}</option>
                </select>
              </div>
              <div class="form-group flex-2">
                <label>플랜명</label>
                <input v-model="formPlan.name" type="text" placeholder="예: Basic Channel Operation" />
              </div>
              <div class="form-group flex-2">
                <label>서브명</label>
                <input v-model="formPlan.subname" type="text" placeholder="예: 베이직 채널 운영" />
              </div>
              <div class="form-group flex-1">
                <label>가격(만원)</label>
                <input v-model="formPlan.price" type="number" placeholder="0" />
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 15px; font-size: 13px;">
              <div>
                <label style="font-weight:bold; margin-bottom:5px; display:block;">추천 대상 선택</label>
                <div style="border:1px solid #eee; padding:10px; border-radius:4px; max-height:100px; overflow-y:auto;">
                  <label v-for="item in recommends" :key="item.id" style="display:block; cursor:pointer;">
                    <input type="checkbox" :value="item.id" v-model="formPlan.recommend_ids"> {{ item.name }}
                  </label>
                </div>
              </div>
              <div>
                <label style="font-weight:bold; margin-bottom:5px; display:block;">운영 목적 선택</label>
                <div style="border:1px solid #eee; padding:10px; border-radius:4px; max-height:100px; overflow-y:auto;">
                  <label v-for="item in operations" :key="item.id" style="display:block; cursor:pointer;">
                    <input type="checkbox" :value="item.id" v-model="formPlan.operation_ids"> {{ item.name }}
                  </label>
                </div>
              </div>
              <div>
                <label style="font-weight:bold; margin-bottom:5px; display:block;">촬영 / 편수 선택</label>
                <div style="border:1px solid #eee; padding:10px; border-radius:4px; max-height:100px; overflow-y:auto;">
                  <label v-for="item in productions" :key="item.id" style="display:block; cursor:pointer;">
                    <input type="checkbox" :value="item.id" v-model="formPlan.production_ids"> {{ item.name }}
                  </label>
                </div>
              </div>
              <div>
                <label style="font-weight:bold; margin-bottom:5px; display:block;">제작 항목 선택</label>
                <div style="border:1px solid #eee; padding:10px; border-radius:4px; max-height:100px; overflow-y:auto;">
                  <label v-for="item in items" :key="item.id" style="display:block; cursor:pointer;">
                    <input type="checkbox" :value="item.id" v-model="formPlan.item_ids"> {{ item.name }}
                  </label>
                </div>
              </div>
            </div>
            <button class="btn-submit" @click="addPlan">요금제 추가하기</button>
          </div>

          <div class="section">
            <h3>등록된 요금제 목록</h3>
            <table class="data-table">
              <thead>
                <tr>
                  <th>종류</th>
                  <th>플랜명</th>
                  <th>서브명</th>
                  <th>가격</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="p in plans" :key="p.id">
                  <td><strong>{{ p.plan_type_name || '미지정' }}</strong></td>
                  <td>{{ p.name }}</td>
                  <td>{{ p.subname }}</td>
                  <td>{{ p.price }}만원</td>
                  <td><button class="btn-delete" @click="deletePlan(p.id)">삭제</button></td>
                </tr>
                <tr v-if="plans.length === 0">
                  <td colspan="5" class="text-center">등록된 데이터가 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 브랜드 클라이언트 탭 -->
        <div v-if="activeTab === 'brandClient'">
          <h2 class="panel-title">브랜드 클라이언트 관리</h2>
          
          <div class="section">
            <h3>새 브랜드 추가</h3>
            <div class="form-row">
              <div class="form-group flex-1">
                <input v-model="formBc.name" type="text" placeholder="브랜드명 입력" />
              </div>
              <div class="form-group flex-1">
                <input v-model="formBc.subtitle" type="text" placeholder="소제목(부가설명) 입력 (선택)" />
              </div>
              <button class="btn-submit" @click="addBrandClient">추가하기</button>
            </div>
          </div>

          <div class="section">
            <h3>등록된 브랜드 목록</h3>
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>브랜드명</th>
                  <th>부가설명</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="bc in brandClients" :key="bc.id">
                  <template v-if="editingBrandClientId === bc.id">
                    <td>{{ bc.id }}</td>
                    <td>
                      <input type="text" v-model="editingBrandClientData.name" style="width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px;" />
                    </td>
                    <td>
                      <input type="text" v-model="editingBrandClientData.subtitle" style="width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px;" />
                    </td>
                    <td>
                      <button class="btn-submit" @click="saveBrandClient" style="padding: 6px 12px; font-size: 12px; margin-right: 5px; height: auto;">저장</button>
                      <button class="btn-delete" @click="cancelEditingBrandClient" style="padding: 6px 12px; font-size: 12px; height: auto; background-color: #888;">취소</button>
                    </td>
                  </template>
                  <template v-else>
                    <td>{{ bc.id }}</td>
                    <td>{{ bc.name }}</td>
                    <td>{{ bc.subtitle || '-' }}</td>
                    <td>
                      <button class="btn-submit" @click="startEditingBrandClient(bc)" style="padding: 6px 12px; font-size: 12px; margin-right: 5px; height: auto; background-color: #f39c12;">수정</button>
                      <button class="btn-delete" @click="deleteBrandClient(bc.id)" style="padding: 6px 12px; font-size: 12px; height: auto;">삭제</button>
                    </td>
                  </template>
                </tr>
                <tr v-if="brandClients.length === 0">
                  <td colspan="4" class="text-center">등록된 데이터가 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 납품 프로젝트 탭 -->
        <div v-if="activeTab === 'project'">
          <h2 class="panel-title">납품 프로젝트 관리</h2>
          
          <div class="section">
            <h3>새 프로젝트 추가</h3>
            <div class="form-row">
              <div class="form-group flex-2">
                <input v-model="formProject.title" type="text" placeholder="프로젝트명 입력" />
              </div>
              <div class="form-group flex-2">
                <input v-model="formProject.subtitle" type="text" placeholder="소제목(부가설명) 입력 (선택)" />
              </div>
              <div class="form-group flex-1">
                <select v-model="formProject.client">
                  <option value="">클라이언트 선택 (선택사항)</option>
                  <option v-for="bc in brandClients" :key="bc.id" :value="bc.id">{{ bc.name }}</option>
                </select>
              </div>
              <button class="btn-submit" @click="addProject">추가하기</button>
            </div>
          </div>

          <div class="section">
            <h3>등록된 프로젝트 목록</h3>
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>프로젝트명</th>
                  <th>부가설명</th>
                  <th>클라이언트</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="p in projects" :key="p.id">
                  <template v-if="editingProjectId === p.id">
                    <td>{{ p.id }}</td>
                    <td>
                      <input type="text" v-model="editingProjectData.title" style="width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px;" />
                    </td>
                    <td>
                      <input type="text" v-model="editingProjectData.subtitle" style="width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px;" />
                    </td>
                    <td>
                      <select v-model="editingProjectData.client" style="width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px;">
                        <option value="">선택 안함</option>
                        <option v-for="bc in brandClients" :key="bc.id" :value="bc.id">{{ bc.name }}</option>
                      </select>
                    </td>
                    <td>
                      <button class="btn-submit" @click="saveProject" style="padding: 6px 12px; font-size: 12px; margin-right: 5px; height: auto;">저장</button>
                      <button class="btn-delete" @click="cancelEditingProject" style="padding: 6px 12px; font-size: 12px; height: auto; background-color: #888;">취소</button>
                    </td>
                  </template>
                  <template v-else>
                    <td>{{ p.id }}</td>
                    <td>{{ p.title }}</td>
                    <td>{{ p.subtitle || '-' }}</td>
                    <td>{{ p.client_name || '-' }}</td>
                    <td>
                      <button class="btn-submit" @click="startEditingProject(p)" style="padding: 6px 12px; font-size: 12px; margin-right: 5px; height: auto; background-color: #f39c12;">수정</button>
                      <button class="btn-delete" @click="deleteProject(p.id)" style="padding: 6px 12px; font-size: 12px; height: auto;">삭제</button>
                    </td>
                  </template>
                </tr>
                <tr v-if="projects.length === 0">
                  <td colspan="5" class="text-center">등록된 데이터가 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 카테고리 탭 -->
        <div v-if="activeTab === 'category'">
          <h2 class="panel-title">카테고리 관리</h2>
          
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px;">
            <!-- 대분류 관리 -->
            <div>
              <div class="section">
                <h3>새 대분류 추가</h3>
                <div class="form-row" style="align-items: flex-end; margin-bottom: 20px;">
                  <div class="form-group flex-2">
                    <label>대분류명 *</label>
                    <input v-model="formMainCategory.name" type="text" placeholder="예: 영상, 브랜드" />
                  </div>
                  <div class="form-group flex-1">
                    <label>노출 순서</label>
                    <input v-model="formMainCategory.order" type="number" placeholder="0" />
                  </div>
                  <button class="btn-submit" @click="addMainCategory">추가</button>
                </div>

                <table class="data-table">
                  <thead>
                    <tr>
                      <th style="width: 50px;">순서</th>
                      <th>대분류명</th>
                      <th>관리</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="cat in mainCategories" :key="'mc-'+cat.id">
                      <template v-if="editingMainCategoryId === cat.id">
                        <td><input type="number" v-model="editingMainCategoryData.order" style="width:100%; padding:4px;" /></td>
                        <td><input type="text" v-model="editingMainCategoryData.name" style="width:100%; padding:4px;" /></td>
                        <td>
                          <button class="btn-submit" @click="saveMainCategory" style="padding: 4px 8px; font-size:11px;">저장</button>
                          <button class="btn-delete" @click="cancelEditingMainCategory" style="padding: 4px 8px; font-size:11px; background:#888;">취소</button>
                        </td>
                      </template>
                      <template v-else>
                        <td>{{ cat.order }}</td>
                        <td>{{ cat.name }}</td>
                        <td>
                          <button class="btn-submit" @click="startEditingMainCategory(cat)" style="padding: 4px 8px; font-size:11px; background:#f39c12; margin-right:4px;">수정</button>
                          <button class="btn-delete" @click="deleteMainCategory(cat.id)" style="padding: 4px 8px; font-size:11px;">삭제</button>
                        </td>
                      </template>
                    </tr>
                    <tr v-if="mainCategories.length === 0">
                      <td colspan="3" class="text-center">등록된 대분류가 없습니다.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- 중분류 관리 -->
            <div>
              <div class="section">
                <h3>새 중분류(카테고리) 추가</h3>
                
                <div class="form-row" style="margin-bottom: 15px;">
                  <div class="form-group flex-1">
                    <label>소속 대분류 선택 *</label>
                    <select v-model="formSubCategory.main_category">
                      <option value="">대분류를 먼저 선택하세요</option>
                      <option v-for="mc in mainCategories" :key="'smc-'+mc.id" :value="mc.id">{{ mc.name }}</option>
                    </select>
                  </div>
                  <div class="form-group flex-1">
                    <label>중분류명(카테고리명) *</label>
                    <input v-model="formSubCategory.name" type="text" placeholder="예: 브랜드 필름" />
                  </div>
                  <div class="form-group flex-1">
                    <label>노출 순서</label>
                    <input v-model="formSubCategory.order" type="number" placeholder="0" />
                  </div>
                </div>

                <div class="form-row" style="margin-bottom: 15px; background: #fafafa; padding: 15px; border-radius: 6px; border: 1px solid #eee;">
                  <div class="form-group flex-1" style="display:flex; align-items:center; gap:8px;">
                    <input type="checkbox" id="isSubVertical" v-model="formSubCategory.is_vertical" style="width: 16px; height: 16px;" />
                    <label for="isSubVertical" style="margin:0; cursor:pointer; font-weight: bold; color: #111;">세로형(쇼츠) 여부</label>
                  </div>
                  <div class="form-group flex-1" style="display:flex; align-items:center; gap:8px;">
                    <input type="checkbox" id="isSubInstagram" v-model="formSubCategory.is_instagram" style="width: 16px; height: 16px;" />
                    <label for="isSubInstagram" style="margin:0; cursor:pointer; font-weight: bold; color: #111;">인스타그램 여부</label>
                  </div>
                </div>
                
                <div style="text-align: right; margin-bottom: 20px;">
                  <button class="btn-submit" @click="addSubCategory">중분류 추가하기</button>
                </div>

                <table class="data-table">
                  <thead>
                    <tr>
                      <th style="width: 50px;">순서</th>
                      <th>대분류 / 중분류명</th>
                      <th>설정</th>
                      <th>관리</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="cat in subCategories" :key="'sc-'+cat.id">
                      <template v-if="editingSubCategoryId === cat.id">
                        <td><input type="number" v-model="editingSubCategoryData.order" style="width:100%; padding:4px;" /></td>
                        <td>
                          <select v-model="editingSubCategoryData.main_category" style="width:100%; padding:4px; margin-bottom: 4px;">
                            <option v-for="mc in mainCategories" :key="'esmc-'+mc.id" :value="mc.id">{{ mc.name }}</option>
                          </select>
                          <input type="text" v-model="editingSubCategoryData.name" style="width:100%; padding:4px;" />
                        </td>
                        <td>
                          <label style="display:block; font-size:11px; margin-bottom:4px; cursor:pointer;"><input type="checkbox" v-model="editingSubCategoryData.is_vertical"> 쇼츠</label>
                          <label style="display:block; font-size:11px; cursor:pointer;"><input type="checkbox" v-model="editingSubCategoryData.is_instagram"> 인스타</label>
                        </td>
                        <td>
                          <button class="btn-submit" @click="saveSubCategory" style="padding: 4px 8px; font-size:11px;">저장</button>
                          <button class="btn-delete" @click="cancelEditingSubCategory" style="padding: 4px 8px; font-size:11px; background:#888;">취소</button>
                        </td>
                      </template>
                      <template v-else>
                        <td>{{ cat.order }}</td>
                        <td><span style="color:#888; font-size:12px;">[{{ mainCategories.find(mc => mc.id === cat.main_category)?.name || '' }}]</span><br><b>{{ cat.name }}</b></td>
                        <td style="font-size:12px;">
                          <span v-if="cat.is_vertical" style="color:#1a3ae0; font-weight:bold;">[쇼츠]</span>
                          <span v-if="cat.is_instagram" style="color:#e74c3c; font-weight:bold;">[인스타]</span>
                        </td>
                        <td>
                          <button class="btn-submit" @click="startEditingSubCategory(cat)" style="padding: 4px 8px; font-size:11px; background:#f39c12; margin-right:4px;">수정</button>
                          <button class="btn-delete" @click="deleteSubCategory(cat.id)" style="padding: 4px 8px; font-size:11px;">삭제</button>
                        </td>
                      </template>
                    </tr>
                    <tr v-if="subCategories.length === 0">
                      <td colspan="4" class="text-center">등록된 중분류가 없습니다.</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- 최종 영상 탭 -->
        <div v-if="activeTab === 'work'">
          <h2 class="panel-title">최종 영상 (Work) 관리</h2>
          
          <div class="section">
            <h3>새 영상 포트폴리오 추가</h3>
            
            <!-- 플랫폼 선택 -->
            <div class="form-row" style="margin-bottom: 15px;">
              <div class="form-group flex-1">
                <label>플랫폼 선택</label>
                <div style="display: flex; gap: 20px; align-items: center; margin-top: 10px;">
                  <label style="display:flex; align-items:center; gap:8px; cursor:pointer; margin:0;"><input type="radio" v-model="selectedPlatform" value="YOUTUBE" /> 유튜브 (YouTube)</label>
                  <label style="display:flex; align-items:center; gap:8px; cursor:pointer; margin:0;"><input type="radio" v-model="selectedPlatform" value="INSTAGRAM" /> 인스타그램 (Instagram)</label>
                </div>
              </div>
            </div>

            <!-- 유튜브 URL 또는 검색 입력부 -->
            <div v-if="selectedPlatform === 'YOUTUBE'" class="form-row" style="margin-bottom: 15px; align-items: flex-end;">
              <div class="form-group flex-1">
                <label>유튜브 영상 링크</label>
                <div style="display:flex; gap:10px;">
                  <input v-model="formWork.youtube_link" type="text" placeholder="https://www.youtube.com/watch?v=..." />
                  <button class="btn-submit" @click="fetchYoutubeInfo" style="background-color: #f00;">링크로 불러오기</button>
                </div>
              </div>
              <div class="form-group flex-1" style="position: relative;">
                <label>또는 유튜브 검색</label>
                <div style="display:flex; gap:10px;">
                  <input v-model="searchQuery" type="text" placeholder="검색어 입력 후 Enter" @keyup.enter="searchYoutube" />
                  <button class="btn-submit" @click="searchYoutube" style="background-color: #333;">{{ isSearching ? '검색중...' : '검색' }}</button>
                </div>
                
                <!-- 검색 결과 드롭다운 -->
                <div v-if="searchResults.length > 0" class="search-results-dropdown">
                  <div class="search-close-btn" @click="searchResults = []">✕ 닫기</div>
                  <div v-for="res in searchResults" :key="res.video_id" class="search-result-item" @click="selectYoutubeResult(res)">
                    <img :src="res.thumbnail_url" alt="thumbnail" class="result-thumb" />
                    <div class="result-title">{{ res.title }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 인스타그램 퍼가기 코드 입력부 추가 -->
            <div v-if="selectedPlatform === 'INSTAGRAM'" class="form-row" style="margin-bottom: 15px;">
              <div class="form-group flex-1">
                <label>인스타그램 퍼가기 코드 (HTML)</label>
                <textarea v-model="formWork.instagram_embed" rows="3" placeholder="인스타그램 게시물에서 '퍼가기' 버튼을 눌러 복사한 HTML 코드를 붙여넣으세요. 유튜브 링크와 함께 입력된 경우 인스타그램 카드가 우선 표시됩니다."></textarea>
              </div>
            </div>

            <!-- 미리보기 썸네일 -->
            <div v-if="formWork.thumbnail_url" style="margin-bottom: 15px;">
              <img :src="formWork.thumbnail_url" alt="미리보기" style="max-height: 150px; border-radius: 8px; border: 1px solid #ddd;" />
            </div>

            <!-- 세부 입력 폼 -->
            <div class="form-row" style="margin-bottom: 15px;">
              <div class="form-group flex-2">
                <label>작품명(제목) *</label>
                <input v-model="formWork.title" type="text" placeholder="작품명 입력 (유튜브 연동 시 자동 입력됨)" />
              </div>
              <div class="form-group flex-1">
                <label>소속 중분류(카테고리) *</label>
                <select v-model="formWork.sub_category">
                  <option value="">카테고리 선택</option>
                  <optgroup v-for="mc in mainCategories" :key="'mc-'+mc.id" :label="mc.name">
                    <option v-for="sc in subCategories.filter(s => s.main_category === mc.id)" :key="'sc-'+sc.id" :value="sc.id">
                      {{ sc.name }}
                    </option>
                  </optgroup>
                </select>
              </div>
            </div>

            <div class="form-row" style="margin-bottom: 15px;">
              <div class="form-group flex-1">
                <label>게시글 내용 (선택)</label>
                <textarea v-model="formWork.content" rows="3" placeholder="간략한 설명이나 참여 스태프 정보 등을 적어주세요"></textarea>
              </div>
            </div>

            <div class="form-row" style="margin-bottom: 15px;">
              <div class="form-group flex-1">
                <label>진행 상태</label>
                <select v-model="formWork.status">
                  <option value="IN_PROGRESS">작업중 (In Progress)</option>
                  <option value="COMPLETED">완료됨 (Completed)</option>
                </select>
              </div>
              <div class="form-group flex-1" style="display: flex; align-items: center; gap: 10px; margin-top: 25px;">
                <input type="checkbox" id="isVisible" v-model="formWork.is_visible" />
                <label for="isVisible" style="margin:0; font-weight:600; cursor:pointer;">홈페이지 공개 여부</label>
              </div>
              <div class="flex-1" style="text-align:right; margin-top: 20px;">
                <button class="btn-submit" @click="addWork">영상 추가하기</button>
              </div>
            </div>
          </div>

          <div class="section">
            <h3>등록된 영상 목록 (총 {{ works.length }}개)</h3>
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>카테고리</th>
                  <th>작품명</th>
                  <th>상태</th>
                  <th>공개</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="w in works" :key="w.id">
                  <td>{{ w.id }}</td>
                  <td>{{ w.sub_category_name || '-' }}</td>
                  <td>
                    <span v-if="w.youtube_link" @click="playVideo(w.youtube_link)" style="color:#1a3ae0; font-weight:600; cursor:pointer; text-decoration:underline;">
                      ▶ {{ w.title }}
                    </span>
                    <span v-else>{{ w.title }}</span>
                  </td>
                  <td>
                    <select v-model="w.status" @change="updateWorkStatus(w)" style="padding: 5px; font-size: 12px; font-weight: bold; width: 100px;" :style="{ color: w.status === 'COMPLETED' ? '#27ae60' : '#f39c12', borderColor: w.status === 'COMPLETED' ? '#27ae60' : '#f39c12' }">
                      <option value="IN_PROGRESS" style="color: #f39c12;">작업중</option>
                      <option value="COMPLETED" style="color: #27ae60;">완료됨</option>
                    </select>
                  </td>
                  <td>
                    <div style="display:flex; justify-content:center; align-items:center; height:100%;">
                      <input type="checkbox" v-model="w.is_visible" @change="updateWorkVisibility(w)" style="cursor:pointer; width:16px; height:16px;" />
                    </div>
                  </td>
                  <td><button class="btn-delete" @click="deleteWork(w.id)">삭제</button></td>
                </tr>
                <tr v-if="works.length === 0">
                  <td colspan="6" class="text-center">등록된 데이터가 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 문의 내역 탭 -->
        <div v-if="activeTab === 'inquiry'">
          <h2 class="panel-title">문의 내역 관리</h2>
          
          <div class="section">
            <h3>접수된 문의 목록 (총 {{ inquiries.length }}건)</h3>
            <table class="data-table">
              <thead>
                <tr>
                  <th>확인여부</th>
                  <th>등록일</th>
                  <th>제목 / 연락처 / 카테고리</th>
                  <th>상세 내용</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="inq in inquiries" :key="inq.id">
                  <td style="text-align:center;">
                    <button 
                      @click="toggleInquiryRead(inq)"
                      style="border:none; padding:4px 8px; border-radius:4px; font-size:12px; cursor:pointer;"
                      :style="{ backgroundColor: inq.is_read ? '#eee' : '#1a3ae0', color: inq.is_read ? '#666' : '#fff' }"
                    >
                      {{ inq.is_read ? '읽음' : '새 문의' }}
                    </button>
                  </td>
                  <td>{{ new Date(inq.created_at).toLocaleDateString() }}</td>
                  <td>
                    <div style="font-weight:bold; margin-bottom:4px;">{{ inq.title }}</div>
                    <div style="font-size:12px; color:#666;">
                      {{ inq.name }} ({{ inq.company || '소속없음' }})<br>
                      {{ inq.phone }} | {{ inq.email || '이메일없음' }}<br>
                      [{{ inq.category || '카테고리없음' }}] 예산: {{ inq.budget }}
                    </div>
                  </td>
                  <td>
                    <div style="font-size:13px; max-width:300px; white-space:pre-wrap;">{{ inq.details || '-' }}</div>
                  </td>
                  <td>
                    <div style="display:flex; align-items:center; gap:8px;">
                      <select v-model="inq.status" @change="updateInquiryStatus(inq)" style="padding: 4px; font-size: 12px; font-weight: bold; width: 100px; border-radius: 4px;" :style="{ color: inq.status === 'COMPLETED' ? '#27ae60' : inq.status === 'IN_PROGRESS' ? '#f39c12' : '#e74c3c', borderColor: inq.status === 'COMPLETED' ? '#27ae60' : inq.status === 'IN_PROGRESS' ? '#f39c12' : '#e74c3c' }">
                        <option value="UNPROCESSED" style="color: #e74c3c;">미접수</option>
                        <option value="IN_PROGRESS" style="color: #f39c12;">처리 중</option>
                        <option value="COMPLETED" style="color: #27ae60;">처리 완료</option>
                      </select>
                      <button class="btn-delete" @click="deleteInquiry(inq.id)">삭제</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="inquiries.length === 0">
                  <td colspan="5" class="text-center">접수된 문의 내역이 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 사이트 설정 탭 -->
        <div v-if="activeTab === 'siteSetting'">
          <h2 class="panel-title">사이트 설정 (로고 및 메인 섹션 관리)</h2>
          
          <div class="section">
            <h3>메인 섹션 노출 및 헤더 설정</h3>
            <p style="font-size:13px; color:#666; margin-bottom:15px;">홈페이지 각 섹션의 노출 여부와 상단 괄호 안의 제목을 설정합니다. (인덱스 번호는 켜진 순서대로 01, 02, 03 자동 부여)</p>

            <!-- Service 설정 -->
            <div style="border:1px solid #eee; padding:15px; border-radius:8px; margin-bottom:15px; background-color: #fafafa;">
              <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px; font-weight:bold;">
                <input type="checkbox" id="svc_visible" v-model="siteSetting.is_service_visible" style="width: 16px; height: 16px;" />
                <label for="svc_visible" style="margin:0; cursor:pointer; color: #1a3ae0;">Service 섹션 노출하기</label>
              </div>
              <div class="form-row">
                <div class="form-group flex-1">
                  <label>Service 섹션 메인 타이틀 (예: MONTHLY PLAN)</label>
                  <input v-model="siteSetting.service_title" type="text" />
                </div>
                <div class="form-group flex-1">
                  <label>Service 서브 설명 (예: 영상 운영 가격 / 한달 기준)</label>
                  <input v-model="siteSetting.service_desc" type="text" />
                </div>
              </div>
            </div>

            <!-- About 설정 -->
            <div style="border:1px solid #eee; padding:15px; border-radius:8px; margin-bottom:15px; background-color: #fafafa;">
              <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px; font-weight:bold;">
                <input type="checkbox" id="abt_visible" v-model="siteSetting.is_about_visible" style="width: 16px; height: 16px;" />
                <label for="abt_visible" style="margin:0; cursor:pointer; color: #1a3ae0;">About 섹션 노출하기</label>
              </div>
              <div class="form-row">
                <div class="form-group flex-1">
                  <label>About 섹션 메인 타이틀 (예: ABOUT THE STUDIO)</label>
                  <input v-model="siteSetting.about_title" type="text" />
                </div>
                <div class="form-group flex-1">
                  <label>About 서브 설명 (예: 하이어, 더 높은 곳으로)</label>
                  <input v-model="siteSetting.about_desc" type="text" />
                </div>
              </div>
            </div>

            <!-- Contact / Footer 설정 -->
            <div style="border:1px solid #eee; padding:15px; border-radius:8px; margin-bottom:25px; background-color: #fafafa;">
              <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px; font-weight:bold;">
                <input type="checkbox" id="cnt_visible" v-model="siteSetting.is_contact_visible" style="width: 16px; height: 16px;" />
                <label for="cnt_visible" style="margin:0; cursor:pointer; color: #e74c3c;">Contact(Footer) 섹션 노출하기 (※ 주의: 끄면 모든 페이지 하단이 통째로 사라집니다)</label>
              </div>
              <div class="form-row">
                <div class="form-group flex-1">
                  <label>Contact 섹션 메인 타이틀 (예: GET IN TOUCH)</label>
                  <input v-model="siteSetting.contact_header_title" type="text" />
                </div>
                <div class="form-group flex-1">
                  <label>Contact 서브 설명 (예: 하이어, 더 높은 곳으로)</label>
                  <input v-model="siteSetting.contact_header_desc" type="text" />
                </div>
              </div>
            </div>

            <hr style="border:none; border-top:1px solid #eee; margin:40px 0;">

            <h3>사이트 로고 텍스트 변경</h3>
            <p style="font-size:13px; color:#666; margin-bottom:15px;">※ 현재는 데이터베이스(charfield)를 이용한 텍스트 형태의 로고 변경만 지원합니다. 이미지 업로드 기능은 추후 구현됩니다.</p>
            <div class="form-row" style="margin-bottom:15px;">
              <div class="form-group flex-1">
                <label>국문 로고 (logo_kr)</label>
                <input v-model="siteSetting.logo_kr" type="text" placeholder="예: HIGHER PRODUCTION" />
              </div>
            </div>
            <div class="form-row" style="margin-bottom:25px;">
              <div class="form-group flex-1">
                <label>영문 로고 (logo_en)</label>
                <input v-model="siteSetting.logo_en" type="text" placeholder="예: HIGHER PRODUCTION" />
              </div>
            </div>

            <h3 style="margin-top:40px;">About 섹션 제목 변경</h3>
            <p style="font-size:13px; color:#666; margin-bottom:15px;">홈페이지 'ABOUT THE STUDIO' 섹션의 메인 카피를 수정합니다.</p>
            
            <div v-for="(heading, index) in siteSetting.about_headings" :key="index" class="form-row" style="margin-bottom:15px; align-items: center;">
              <div class="form-group flex-2">
                <label>{{ index + 1 }}번째 줄</label>
                <input v-model="heading.text" type="text" placeholder="내용을 입력하세요" />
              </div>
              <div class="form-group" style="margin-top: 25px; display: flex; align-items: center; gap: 8px;">
                <input type="checkbox" :id="'highlight_' + index" v-model="heading.is_highlighted" />
                <label :for="'highlight_' + index" style="margin:0; cursor:pointer;">강조 적용</label>
              </div>
              <div class="form-group" style="margin-top: 25px;">
                <button class="btn-delete" @click="removeAboutHeading(index)">삭제</button>
              </div>
            </div>
            
            <div style="margin-bottom: 25px;">
              <button class="btn-submit" @click="addAboutHeading" style="background-color: #f39c12;">+ 줄 추가하기</button>
            </div>

            <h3 style="margin-top:40px;">연락처 및 하단 정보 (Footer)</h3>
            <p style="font-size:13px; color:#666; margin-bottom:15px;">홈페이지 하단(Footer)에 표시되는 연락처 및 슬로건 정보를 수정합니다.</p>
            
            <label style="display:block; font-size:13px; font-weight:600; color:#555; margin-bottom:5px;">푸터 메인 슬로건 (footer_slogan_main)</label>
            <div v-for="(line, index) in siteSetting.footer_slogan_main" :key="'fs_' + index" class="form-row" style="margin-bottom:10px; align-items:center;">
              <div class="form-group flex-1">
                <input v-model="siteSetting.footer_slogan_main[index]" type="text" placeholder="문장을 입력하세요" />
              </div>
              <div class="form-group" style="margin-bottom:0;">
                <button class="btn-delete" @click="siteSetting.footer_slogan_main.splice(index, 1)">삭제</button>
              </div>
            </div>
            <div style="margin-bottom: 25px;">
              <button class="btn-submit" @click="siteSetting.footer_slogan_main.push('')" style="background-color: #f39c12; padding:8px 15px; width:auto; font-size:13px;">+ 줄 추가하기</button>
            </div>

            <div class="form-row" style="margin-bottom:15px;">
              <div class="form-group flex-1">
                <label>푸터 서브 슬로건 (footer_slogan_sub)</label>
                <input v-model="siteSetting.footer_slogan_sub" type="text" placeholder="예: Let's go higher." />
              </div>
            </div>

            <div class="form-row" style="margin-bottom:15px;">
              <div class="form-group flex-1">
                <label>이메일 (Email)</label>
                <input v-model="siteSetting.email" type="email" placeholder="예: higher3pd@gmail.com" />
              </div>
              <div class="form-group flex-1">
                <label>전화번호 (Phone)</label>
                <input v-model="siteSetting.phone" type="text" placeholder="예: +82 10-3313-0388" />
              </div>
            </div>
            
            <div class="form-row" style="margin-bottom:15px;">
              <div class="form-group flex-1">
                <label>스튜디오 주소 (Address)</label>
                <input v-model="siteSetting.address" type="text" placeholder="예: 경기도 의정부시, KR" />
              </div>
            </div>
            
            <div class="form-row" style="margin-bottom:25px;">
              <div class="form-group flex-1">
                <label>인스타그램 아이디 (Handle)</label>
                <input v-model="siteSetting.instagram_handle" type="text" placeholder="예: @higher.production" />
              </div>
              <div class="form-group flex-2">
                <label>인스타그램 링크 (URL)</label>
                <input v-model="siteSetting.instagram_url" type="url" placeholder="예: https://instagram.com/higher.production" />
              </div>
            </div>

            <h3 style="margin-top:40px;">문의 페이지 (Contact) 설정</h3>
            <p style="font-size:13px; color:#666; margin-bottom:15px;">Contact 페이지 상단의 메인 타이틀을 수정합니다.</p>
            
            <div class="form-row" style="margin-bottom:25px;">
              <div class="form-group flex-1">
                <label>페이지 타이틀 (contact_title)</label>
                <input v-model="siteSetting.contact_title" type="text" placeholder="예: LET'S GO HIGHER" />
              </div>
            </div>

            <button class="btn-submit" @click="saveSiteSetting">설정 저장</button>
          </div>
        </div>

      </main>
    </div>

    <!-- 비디오 모달 (영상 바로 시청) -->
    <div v-if="playingVideoId" class="video-modal-overlay" @click="closeVideo">
      <div class="video-modal-content" @click.stop>
        <button class="video-modal-close" @click="closeVideo">✕ 닫기</button>
        <div class="video-responsive-wrap">
          <iframe 
            :src="`https://www.youtube.com/embed/${playingVideoId}?autoplay=1`" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
          </iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Profile 뷰와 유사한 레이아웃 스타일 */
.profile-layout {
  max-width: 1000px;
  margin: 60px auto;
  padding: 0 20px;
}

.edit-layout {
  max-width: 1200px; /* 에디터는 가로로 좀 더 넓게 */
}

.profile-grid {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 30px;
}

@media (max-width: 768px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}

.dashboard-panel, .profile-panel {
  background-color: white;
  border-radius: 8px;
  padding: 40px 30px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  border: 1px solid #eaeaea;
}

.panel-title {
  margin-bottom: 30px;
  font-weight: 700;
  color: #222;
  font-size: 20px;
  border-bottom: 2px solid #111;
  padding-bottom: 15px;
}

/* 관리자 메뉴 사이드바 */
.admin-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.admin-menu li {
  padding: 15px 20px;
  margin-bottom: 10px;
  background-color: #fafafa;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  color: #555;
  transition: all 0.2s;
  border: 1px solid #eee;
}

.admin-menu li:hover {
  background-color: #f0f0f0;
}

.admin-menu li.active {
  background-color: #1a3ae0;
  color: #fff;
  border-color: #1a3ae0;
}

/* 폼 스타일 */
.section {
  margin-bottom: 40px;
}

.section h3 {
  font-size: 16px;
  font-weight: 700;
  color: #111;
  margin-bottom: 15px;
}

.form-row {
  display: flex;
  gap: 15px;
  align-items: center;
}

.form-group {
  margin-bottom: 0;
}

.flex-1 { flex: 1; }
.flex-2 { flex: 2; }

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #555;
  margin-bottom: 5px;
}

input[type="text"], input[type="email"], input[type="url"], select, textarea {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}

.btn-submit {
  padding: 12px 25px;
  background-color: #111;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.btn-submit:hover {
  background-color: #1a3ae0;
}

/* 테이블 스타일 */
.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
  text-align: left;
  font-size: 14px;
}

.data-table th {
  background-color: #fafafa;
  font-weight: 600;
  color: #444;
}

.btn-delete {
  padding: 6px 12px;
  background-color: #ff4757;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.btn-delete:hover {
  background-color: #ff6b81;
}

.text-center {
  text-align: center;
}

/* 검색 결과 드롭다운 */
.search-results-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  z-index: 100;
  max-height: 350px;
  overflow-y: auto;
  margin-top: 5px;
}

.search-close-btn {
  text-align: right;
  padding: 8px 15px;
  font-size: 12px;
  color: #888;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}
.search-close-btn:hover { color: #f00; }

.search-result-item {
  display: flex;
  gap: 12px;
  padding: 12px 15px;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  align-items: center;
}

.search-result-item:hover {
  background-color: #f9f9f9;
}

.result-thumb {
  width: 100px;
  height: 56px;
  object-fit: cover;
  border-radius: 4px;
}

.result-title {
  font-size: 13px;
  color: #333;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* 비디오 모달 */
.video-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.video-modal-content {
  position: relative;
  width: 90%;
  max-width: 1000px;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.video-modal-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

.video-responsive-wrap {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 비율 */
  height: 0;
  overflow: hidden;
}

.video-responsive-wrap iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
